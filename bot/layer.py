import sys
import time
from text_feedback          import WhatToFeedback
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
from yowsup.layers.auth import YowAuthenticationProtocolLayer


class EchoLayer(YowInterfaceLayer):

    def removeNonAscii(self,s): return "".join(i for i in s if ord(i)<128)

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #send receipt otherwise we keep receiving the same message over and over
            
        receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(), 'read', messageProtocolEntity.getParticipant())
        self.toLower(receipt)
        
        if messageProtocolEntity.getType() == 'text':
            try:
                self.onTextMessage(messageProtocolEntity) 
            except Exception as e:
                print(e)
                print "error on message by "+messageProtocolEntity.getNotify()

            if self.removeNonAscii(messageProtocolEntity.getBody().lower()) == 'init 0':
                time.sleep(3)
                sys.exit(0)
    
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)

    def onTextMessage(self,messageProtocolEntity):
        namemitt   = messageProtocolEntity.getNotify()
        message    = self.removeNonAscii(messageProtocolEntity.getBody().lower())
        recipient  = messageProtocolEntity.getFrom() if not messageProtocolEntity.isGroupMessage() else messageProtocolEntity.getParticipant()
        textmsg    = TextMessageProtocolEntity
        answer     = ""
        
        
            
    #    if messageProtocolEntity.isGroupMessage():
    #        dashpos = recipient.find("@")
    #        if dashpos != -1 :
    #            recipient = recipient[:dashpos]+"@s.whatsapp.net"

        if message == 'init 0':
            answer = "Ok "+namemitt+", shutting down. Bye bye."

        elif message == 'list command':
            answer = """List of command

 *NOVA <query>*

Queries:
  *cmcount* - CM count for each nodes
  *bainfo* <banumber> - BA Summary
"""
        elif message.startswith("nova "):
        
            print "Message from: "+namemitt+"@"+recipient+" - "+message
            if messageProtocolEntity.isGroupMessage():
                print messageProtocolEntity.getFrom()
            
            a = WhatToFeedback()
            answer = a.getFeedback(message)

        if answer != "":
            print "sending to "+recipient+" : "+answer
 
            try:
                self.toLower(textmsg(answer, to = recipient))
            except Exception as e:
                print (e)
                print "unable to reply to "+recipient

