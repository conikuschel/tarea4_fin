from rest_framework import serializers
from subpub.models import Conciliacion, Transaccion


class TransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaccion
        fields=('id', 'tipo', 'banco_origen', 'cuenta_origen', 'banco_destino', 'cuenta_destino', 'monto', 'message_id','fecha',
        )

class ConciliacionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Conciliacion
        fields=('banco_origen', 'banco_destino', 'montos',
        )


