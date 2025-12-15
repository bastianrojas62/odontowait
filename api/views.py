import requests
from datetime import date

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from pacientes.models import Paciente
from .serializers import PacienteSerializer


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all().order_by('id')
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated]


class FeriadosChileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = request.query_params.get("year") or str(date.today().year)

        headers = {
            "User-Agent": "OdontoWait/1.0 (Django; contacto: demo@localhost)",
            "Accept": "application/json",
        }

        # 1) Intento principal: API Gobierno Digital
        url_gob = f"https://apis.digital.gob.cl/fl/feriados/{year}"

        try:
            r = requests.get(url_gob, headers=headers, timeout=15)
            r.raise_for_status()
            data = r.json()
            return Response({
                "fuente": "apis.digital.gob.cl/fl/feriados",
                "year": int(year),
                "total": len(data),
                "feriados": data,
            })
        except Exception as e_gob:
            # 2) Fallback: Boostr (devuelve feriados del año actual en /holidays.json)
            # Nota: si piden otro año, igual devolvemos con advertencia.
            url_boostr = "https://api.boostr.cl/holidays.json"

            try:
                r2 = requests.get(url_boostr, headers=headers, timeout=15)
                r2.raise_for_status()
                data2 = r2.json()
                return Response({
                    "fuente": "api.boostr.cl/holidays.json (fallback)",
                    "year": int(year),
                    "warning": "La fuente principal (Gobierno Digital) no respondió, se usó fallback.",
                    "detalle_falla_fuente_principal": str(e_gob),
                    "total": len(data2),
                    "feriados": data2,
                })
            except Exception as e2:
                return Response(
                    {
                        "error": "No se pudo obtener la información de feriados",
                        "detalle_fuente_principal": str(e_gob),
                        "detalle_fallback": str(e2),
                    },
                    status=502,
                )