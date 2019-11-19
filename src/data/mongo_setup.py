import mongoengine


def global_init():
    #for local mongodb, no encryption, no accounts
    alias = 'core'
    name = 'snake_bnb'
    mongoengine.register_connection(alias = alias ,name = name)