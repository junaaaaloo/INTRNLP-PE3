class QueryBuilder:
    @staticmethod
    def where (condition):
        return "{} {} {} {} ".format(
            condition["column"],
            condition["operator"],
            condition["value"],
            condition["next"] if ("next" in condition) else ""
        )

    @staticmethod
    def set (updated_value):
        return "{} = {}".format(
            updated_value["column"],
            updated_value["value"]
        )

    @staticmethod
    def select(table, columns=None, conditions=None, order=None, group=None):
        return "SELECT {} FROM {} {} {} {}".format(
            "*" if columns == None else ",".join(columns),
            table,
            "" if (conditions == None) else "WHERE {}".format("".join(list(map(QueryBuilder.where, conditions)))),
            "" if (order == None) else "ORDER BY {}".format(",".join(order)),
            "" if (group == None) else "GROUP BY {}".format(",".join(group))
        )

    @staticmethod
    def insert(table, columns):
        return "INSERT INTO {} {} VALUES ({})".format(
            table,
            "" if (columns == None) else "({})".format(",".join(columns)),
            " ".join(["?"]*len(columns))       
        )

    @staticmethod
    def delete(table, conditions):
        return "DELETE FROM {} WHERE {}".format(
            table,
            "WHERE {}".format("".join(list(map(QueryBuilder.where, conditions))))
        )

    @staticmethod
    def update(table, updated_values, conditions = None):
        return "UPDATE {} SET {} {}".format(
            table, 
            ",".join(list(map(QueryBuilder.set, updated_values))),
            "" if (conditions == None) else "WHERE {}".format("".join(list(map(QueryBuilder.where, conditions))))
        )