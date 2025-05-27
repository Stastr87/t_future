from t_client.operation_service.operation_types import OperationTypes

print(OperationTypes.OPERATION_TYPE_BOND_TAX.get_ru_str)
print(OperationTypes.OPERATION_TYPE_BOND_TAX.get_operation_id)

print(OperationTypes(2)._missing_)