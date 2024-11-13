from typing import Dict, List, Optional
from pydantic import BaseModel
from threading import Thread
from multiprocessing import Process

class Banana(BaseModel):
    cor: str
    peso: Optional[float]


class ProcessContext(metaclass=Singleton):
    _bananas_para_catar: List[Banana] = None
    _bananas_classificadas: Dict[str, List[Banana]]
    _peso_total_das_bananas: float
    _banana_mais_pesada: float


class FerrerinhaCatadorDeBanana:

    def _classificar_bananas(self, context: ProcessContext):
        context._bananas_classificadas = {}

        for banana in context._bananas_para_catar:
            if not context._bananas_classificadas.get(banana.cor):
                context._bananas_classificadas[banana.cor] = [banana]
            else:
                context._bananas_classificadas[banana.cor].append(banana)

        return self


    def _classificar_banana_mais_pesada(self, context: ProcessContext):
        if len(context._bananas_para_catar) == 0:
            raise Exception('Não tenho bananas para catar')

        context._banana_mais_pesada = context._bananas_para_catar[0]

        for banana in context._bananas_para_catar:
            if banana.peso > context._banana_mais_pesada.peso:
                context._banana_mais_pesada = banana

        return self


    def _obter_peso_total_das_bananas(self, context: ProcessContext):
        context._peso_total_das_bananas = 0

        for banana in context._bananas_para_catar:
            context._peso_total_das_bananas += banana.peso

        return self


    def processar_bananas(self, bananas: List[Banana]) -> Dict[str, List[Banana]]:
        context = ProcessContext() 
        context._bananas_para_catar = bananas

        p_classifica_banana = Process(target=self._classificar_bananas, args=(context,))
        p_banana_mais_pesada = Process(target=self._classificar_banana_mais_pesada, args=(context,))
        p_peso_total_das_bananas = Process(target=self._obter_peso_total_das_bananas, args=(context,))

        Process.join([
            p_classifica_banana, 
            p_banana_mais_pesada, 
            p_peso_total_das_bananas
        ])

        return {
            'peso': context._peso_total_das_bananas,
            'mais_pesada': context._banana_mais_pesada,
            'classificadas': context._bananas_classificadas,
        }