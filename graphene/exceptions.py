from graphenestorage.exceptions import WrongMasterPasswordException as GrapheneWrongMasterPasswordException


class WrongMasterPasswordException(GrapheneWrongMasterPasswordException):
    """ A wrong password was provided
    """
    pass


class WalletExists(Exception):
    """ A wallet has already been created and requires a password to be
        unlocked by means of :func:`graphene.wallet.unlock`.
    """
    pass


class WalletLocked(Exception):
    """ Wallet is locked
    """
    pass


class RPCConnectionRequired(Exception):
    """ An RPC connection is required
    """
    pass


class AccountExistsException(Exception):
    """ The requested account already exists
    """
    pass


class AccountDoesNotExistsException(Exception):
    """ The account does not exist
    """
    pass


class InsufficientAuthorityError(Exception):
    """ The transaction requires signature of a higher authority
    """
    pass


class MissingKeyError(Exception):
    """ A required key couldn't be found in the wallet
    """
    pass


class InvalidWifError(Exception):
    """ The provided private Key has an invalid format
    """
    pass


class NoWalletException(Exception):
    """ No Wallet could be found, please use :func:`graphene.wallet.create` to
        create a new wallet
    """
    pass


class InvalidMessageSignature(Exception):
    """ The message signature does not fit the message
    """
    pass


class KeyNotFound(Exception):
    """ Key not found
    """
    pass


class OfflineHasNoRPCException(Exception):
    """ When in offline mode, we don't have RPC
    """
    pass


class KeyAlreadyInStoreException(Exception):
    """ The key is already stored in the store
    """
    pass
