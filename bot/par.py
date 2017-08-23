from yowsup.stacks                             import YowStackBuilder
from yowsup.common                             import YowConstants
from yowsup.layers                             import YowLayerEvent
from layer                                     import EchoLayer
from yowsup.layers.auth                        import YowAuthenticationProtocolLayer
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.env                                import YowsupEnv

#Uncomment to log
#import logging
#logging.basicConfig(level=logging.DEBUG)

CREDENTIALS = ("60104580404", "+N1soMtuAwwfRBOXdPC9S1otpN0=") # replace with your phone and password

if __name__==  "__main__":

    def theListenerThread(stack):
        print "listener started"

        try:
            stack.loop( timeout = 0.5, discrete = 0.5 )   
        except Exception as e:
            print(e)
            print "server init 0"

    stackBuilder = YowStackBuilder()

    stack = stackBuilder\
        .pushDefaultLayers(True)\
        .push(EchoLayer)\
        .build()

    stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, CREDENTIALS)       #setting credentials
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))          #sending the connect signal
    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])           #whatsapp server address
    stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
    stack.setProp(YowCoderLayer.PROP_RESOURCE, YowsupEnv.getCurrent().getResource())  #info about us as WhatsApp client

    theListenerThread(stack)


