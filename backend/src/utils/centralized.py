class Centralized:

    @staticmethod
    def apply_filters(query, model, filters): 
        for field, value in filters.items():
            column = getattr(model, field, None)

            if column is None:
                continue
            elif isinstance(value, (list, tuple, set)):
                query = query.where(column.in_(value))
            else:
                query = query.where(column==value)
        
        return query
