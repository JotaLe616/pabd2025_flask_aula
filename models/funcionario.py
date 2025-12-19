from dataclasses import dataclass, asdict
from datetime import datetime, date
from typing import Optional 

@dataclass
class Funcionario:

    _cpf: str
    _pnome: str
    _unome: str
    _data_nasc: date
    _endereco: str = 'Macau-Rn'
    _salario: float = 1518.01
    _sexo: str = 'f'
    _cpf_supervisor: Optional[str] = None
    _numero_departamento: Optional[int] = None
    _created_at: Optional[datetime] = None
    _updated_at: Optional[datetime] = None

    # Funcionario -> JSON (dict)
    def to_dict(self) -> dict:
        return asdict(self)

    # JSON (dict) -> Funcionario
    @classmethod
    def from_dict(self, data: dict) -> 'Funcionario':
        return Funcionario(
            data.get('cpf'),
            data.get('pnome'),
            data.get('unome'),
            data.get('data_nasc'),
            data.get('endereco'),
            data.get('salario'),
            data.get('sexo'),
            data.get('cpf_supervisor'),
            data.get('numero_departamento'),
            data.get('created_at'),
            data.get('updated_at')
        )
    
    def __str__(self) -> str:
        return (
            f'Funcionario(cpf={self._cpf}, pnome={self._pnome}, unome={self._unome}, '
            f'data_nasc={self._data_nasc}, endereco={self._endereco}, salario={self._salario}, '
            f'sexo={self._sexo}, cpf_supervisor={self._cpf_supervisor}, '
            f'numero_departamento={self._numero_departamento}, '
            f'created_at={self._created_at}, updated_at={self._updated_at})'
        )

    @property
    def cpf(self) -> str:
        return self._cpf
    
    @cpf.setter
    def cpf(self, cpf: str):
        self._cpf = cpf
        self._updated_at = datetime.now()

    @property
    def pnome(self) -> str:
        return self._pnome
    
    @pnome.setter
    def pnome(self, pnome: str):
        self._pnome = pnome
        self._updated_at = datetime.now()

    @property
    def unome(self) -> str:
        return self._unome

    @unome.setter
    def unome(self, unome: str):
        self._unome = unome
        self._updated_at = datetime.now()

    @property
    def salario(self) -> float:
        return self._salario

    @salario.setter
    def salario(self, salario: float):
        self._salario = salario
        self._updated_at = datetime.now()

    @property
    def data_nasc(self) -> date:
        return self._data_nasc

    @data_nasc.setter
    def data_nasc(self, data_nasc: date):
        self._data_nasc = data_nasc
        self._updated_at = datetime.now()

    @property
    def endereco(self) -> str:
        return self._endereco

    @endereco.setter
    def endereco(self, endereco: str):
        self._endereco = endereco
        self._updated_at = datetime.now()

    @property
    def sexo(self) -> str:
        return self._sexo

    @sexo.setter
    def sexo(self, sexo: str):
        self._sexo = sexo
        self._updated_at = datetime.now()

    @property
    def cpf_supervisor(self) -> Optional[str]:
        return self._cpf_supervisor

    @cpf_supervisor.setter
    def cpf_supervisor(self, cpf_supervisor: Optional[str]):
        self._cpf_supervisor = cpf_supervisor
        self._updated_at = datetime.now()

    @property
    def numero_departamento(self) -> Optional[int]:
        return self._numero_departamento

    @numero_departamento.setter
    def numero_departamento(self, numero_departamento: Optional[int]):
        self._numero_departamento = numero_departamento
        self._updated_at = datetime.now()

    @property
    def created_at(self) -> Optional[datetime]:
        return self._created_at

    @property
    def updated_at(self) -> Optional[datetime]:
        return self._updated_at