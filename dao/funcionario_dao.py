from supabase import Client
from dao.base_dao import BaseDAO
from models.funcionario import Funcionario

class FuncionarioDAO(BaseDAO[Funcionario]):

  def __init__(self, client: Client):
    super().__init__(client, 'funcionario')

  def to_model(self, data: dict) -> Funcionario:
    return Funcionario.from_dict(data)

  def to_dict(self, model: Funcionario) -> dict:
    return model.to_dict()