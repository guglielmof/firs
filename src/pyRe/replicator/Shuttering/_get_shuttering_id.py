def _get_shuttering_id(self):
    """
    build the shuttering id
    """

    return f"{self.collection_name}_{self.nShards}_{self.sampling}_{self.emptyShards}"
