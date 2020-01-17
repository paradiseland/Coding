import xlrd


def get_parameters(file_name):
    """
    from xls file,read the location, demand, trunk types.etc parameters
    """
    wb = xlrd.open_workbook(file_name)
    sheet_10customers = wb.sheet_by_index(1)
    sheet_30customers = wb.sheet_by_index(2)
    sheet_80customers = wb.sheet_by_index(3)
    sheet_300customers = wb.sheet_by_index(4)
    sheet_trunks = wb.sheet_by_index(5)
    sheet_customers = [sheet_10customers, sheet_30customers,
                       sheet_80customers, sheet_300customers]
    num_of_customer = [10, 30, 80, 300]
    location = []
    demand_weight = []
    demand_volume = []
    for index, sheet in enumerate(sheet_customers):
        location.append([(m, n) for m, n in zip(
            sheet.col_values(1), sheet.col_values(2))])
        del location[index][0]
        demand_weight.append([w for w in sheet.col_values(3)])
        demand_volume.append([v for v in sheet.col_values(4)])
        del demand_weight[index][0]
        del demand_volume[index][0]

    info = [0]*4
    for i in range(len(info)):
        info[i] = {"num_of_customer": num_of_customer[i], "location": location[i],
                   "demand_weight": demand_weight[i], "demand_volume": demand_volume[i]}
    trunks_type = [(m, n) for m, n in zip(
        sheet_trunks.col_values(1), sheet_trunks.col_values(2))]
    del trunks_type[0]

    return info, trunks_type


if __name__ == "__main__":
    file_name = "assignment.xls"
    info, trunk = get_parameters(file_name)
    print(trunk)
    print(info["demand_volume"])
