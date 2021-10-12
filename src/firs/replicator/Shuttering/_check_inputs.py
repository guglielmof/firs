def _check_inputs(self, **kwargs):


    # function used to check whether the required inputs have been specified
    if 'sampling' not in kwargs:
        raise AttributeError("sampling strategy not specified")
    elif kwargs['sampling'] not in ['RNDM', 'EVEN']:
        raise ValueError(f"{kwargs['sampling']} is not a valid sampling label.")
    else:
        self.sampling = kwargs['sampling']

    # number of shards
    if 'nShards' not in kwargs:
        raise AttributeError("number of shards not specified.")
    elif type(kwargs['nShards']) is not int or kwargs['nShards'] < 1:
        raise ValueError(f"{kwargs['nShards']} is not a valid number of shard (use integer greater than 1).")
    else:
        self.nShards = kwargs['nShards']


    # empty shards
    if 'emptyShards' not in kwargs:
        raise AttributeError("whether empty shards are allowed is not specified.")

    elif kwargs['emptyShards'] not in ["NE", "E"]:
        raise ValueError(f"{kwargs['nShards']} is not a valid ``emptyShard'' label.")
    else:
        self.emptyShards = kwargs['emptyShards']
