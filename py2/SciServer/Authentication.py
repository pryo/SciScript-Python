__author__ = 'gerard,mtaghiza'
#Python v3.4

import json
import sys
import requests
import os.path
import warnings

from SciServer import Config



class KeystoneUser:
    """
    The class KeystoneUser stores the 'id' and 'name' of the user.
    """
    id = None
    userName = None

class Token:
    """
    The class token stores the authentication token of the user in a particular session.
    """
    value = None


token = Token();

def getKeystoneUserWithToken(token):
    """
    Returns the name and Keystone id of the user corresponding to the specified token.

    :param token: Sciserver's authentication token (string) for the user.
    :return: Returns a KeystoneUser object, which stores the name and id of the user.
    :raises: Throws an exception if the HTTP request to the Authentication URL returns an error.
    :example: token = Authentication.getKeystoneUserWithToken(Authentication.getToken())

    .. seealso:: Authentication.getToken, Authentication.login, Authentication.setToken.
    """
    loginURL = Config.AuthenticationURL
    if ~loginURL.endswith("/"):
        loginURL = loginURL + "/"
    loginURL = loginURL + token

    getResponse = requests.get(loginURL)
    if getResponse.status_code != 200:
        raise Exception("Error when getting the keystone user with token " + str(token) +".\nHttp Response from the Authentication API returned status code " + str(getResponse.status_code) + ":\n" + getResponse.content.decode());

    responseJson = json.loads((getResponse.content.decode()))

    ksu = KeystoneUser()
    ksu.userName = responseJson["token"]["user"]["name"]
    ksu.id = responseJson["token"]["user"]["id"]

    return ksu


def login(UserName, Password):
    """
    Logs the user into SciServer and returns the authentication token.
    This function is useful when SciScript-Python library methods are executed outside the SciServer-Compute environment.
    In this case, the session authentication token does not exist (and therefore can't be automatically recognized),
    so the user has to use Authentication.login in order to log into SciServer manually and get the authentication token.
    Authentication.login also sets the token value in the python instance argument variable "--ident", and as the local object Authentication.token (of class Authentication.Token).

    :param UserName: name of the user (string)
    :param Password: password of the user (string)
    :return: authentication token (string)
    :raises: Throws an exception if the HTTP request to the Authentication URL returns an error.
    :example: token = Authentication.login('loginName','loginPassword')

    .. seealso:: Authentication.getKeystoneUserWithToken, Authentication.getToken, Authentication.setToken, Authentication.token.
    """
    loginURL = Config.AuthenticationURL

    authJson = {"auth":{"identity":{"password":{"user":{"name":UserName,"password":Password}}}}}

    data = json.dumps(authJson).encode()

    headers={'Content-Type': "application/json"}

    postResponse = requests.post(loginURL,data=data,headers=headers)
    if postResponse.status_code != 200:
        raise Exception("Error when logging in. Http Response from the Authentication API returned status code " + str(postResponse.status_code) + ":\n" + postResponse.content.decode());

    _token = postResponse.headers['X-Subject-Token']
    setToken(_token)
    return _token

def getToken():
    """
    Returns the SciServer authentication token of the user. First, will try to return Authentication.token.value.
    If Authentication.token.value is not set, Authentication.getToken will try to return the token value in the python instance argument variable "--ident".
    If this variable does not exist, will try to return the token stored in Config.KeystoneTokenFilePath. Will return a None value if all previous steps fail.

    :return: authentication token (string)
    :example: token = Authentication.getToken()

    .. seealso:: Authentication.getKeystoneUserWithToken, Authentication.login, Authentication.setToken, Authentication.token.

    """
    try:
        if token.value is not None:
            return token.value
        else:
            _token = None
            ident = identArgIdentifier()
            for arg in sys.argv:
                if (arg.startswith(ident)):
                    _token = arg[len(ident):]

            if _token is not None and _token != "":
                setToken(_token)
                return _token
            else:
                tokenFile = Config.KeystoneTokenPath; # '/home/idies/keystone.token'
                if os.path.isfile(tokenFile) :
                    with open(tokenFile, 'r') as f:
                        _token = f.read().rstrip('\n')
                        if _token is not None and _token != "":
                            setToken(_token)
                            return _token
                        else:
                            warnings.warn("In Authentication.getToken: Keystone token is not defined. Returning a None token value. Keystone token is not stored in the command line argument --ident, nor in the system token file " + str(Config.KeystoneTokenPath) + ".", Warning, stacklevel=2)
                            return None;
    except Exception as e:
        raise e;


def setToken(_token):
    """
    Sets the SciServer authentication token of the user in the variable Authentication.token.value, as well as in the python instance argument variable "--ident".

    :param _token: Sciserver's authentication token for the user (string)
    :example: Authentication.setToken('myToken')

    .. seealso:: Authentication.getKeystoneUserWithToken, Authentication.login, Authentication.getToken, Authentication.token.
    """
    if _token is None:
        warnings.warn("Authentication token is being set with a None value.", Warning, stacklevel=2)
    if _token == "":
        warnings.warn("Authentication token is being set as an empty string.", Warning, stacklevel=2)

    token.value = _token;

    found = False
    ident = identArgIdentifier()
    for arg in sys.argv:
        if (arg.startswith(ident)):
            sys.argv.remove(arg)
            sys.argv.append(ident + _token)
            found = True
    if not found:
        sys.argv.append(ident + _token)



def identArgIdentifier():
    """
    Returns the name of the python instance argument variable where the user token is stored.

    :return: name (string) of the python instance argument variable where the user token is stored.
    :example: name = Authentication.identArgIdentifier()

    .. seealso:: Authentication.getKeystoneUserWithToken, Authentication.login, Authentication.getToken, Authentication.token.
    """
    return "--ident="


def getKeystoneToken():
    """
    .. warning:: Deprecated. Use Authentication.getToken instead.

    Returns the users keystone token passed into the python instance with the --ident argument.

    :return: authentication token (string)
    :example: token = Authentication.getKeystoneToken()

    .. seealso:: Authentication.getKeystoneUserWithToken, Authentication.login, Authentication.setToken, Authentication.token, Authentication.getToken.
    """
    warnings.warn("Using SciServer.Authentication.getKeystoneToken is deprecated. Use SciServer.Authentication.getToken instead.", DeprecationWarning, stacklevel=2)

    _token = None
    ident = identArgIdentifier()
    for arg in sys.argv:
        if (arg.startswith(ident)):
            _token = arg[len(ident):]

    #if (_token == ""):
    #    raise EnvironmentError("Keystone token is not in the command line argument --ident.")
    if _token is None or _token == "":
        warnings.warn("Keystone token is not defined, and is not stored in the command line argument --ident.", Warning, stacklevel=2)

    return _token


def setKeystoneToken(_token):
    """
    .. warning:: Deprecated. Use Authentication.setToken instead.

    Sets the token as the --ident argument

    :param _token: authentication token (string)
    :example: Authentication.setKeystoneToken("myToken")

    .. seealso:: Authentication.getKeystoneUserWithToken, Authentication.login, Authentication.setToken, Authentication.token, Authentication.getToken.
    """
    warnings.warn("Using SciServer.Authentication.setKeystoneToken is deprecated. Use SciServer.Authentication.setToken instead.", DeprecationWarning, stacklevel=2)

    if _token is None:
        warnings.warn("Authentication token is being set with a None value.", Warning, stacklevel=2)
    if _token == "":
        warnings.warn("Authentication token is being set as an empty string.", Warning, stacklevel=2)

    found = False
    ident = identArgIdentifier()
    for arg in sys.argv:
        if (arg.startswith(ident)):
            sys.argv.remove(arg)
            sys.argv.append(ident + str(_token))
            found = True
    if not found:
        sys.argv.append(ident + str(_token))
