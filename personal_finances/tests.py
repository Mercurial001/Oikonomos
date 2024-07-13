def adjustable_index(dynamic_number, constant_number):
    if dynamic_number > constant_number:
        # if len(fund_net_flow_objects) > 10
        indexer = dynamic_number - constant_number
        if indexer > constant_number:
            return constant_number
        else:
            return indexer
    else:
        return 0


print(adjustable_index(10, 10))

