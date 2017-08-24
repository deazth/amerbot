import sys
import time
from text_feedback          import WhatToFeedback
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity


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
            except Exception:
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
        recipient  = messageProtocolEntity.getFrom()
        textmsg    = TextMessageProtocolEntity
        answer     = ""
            
        print "Message from: "+namemitt+"@"+recipient+" - "+message

    #    if messageProtocolEntity.isGroupMessage():
    #        dashpos = recipient.find("@")
    #        if dashpos != -1 :
    #            recipient = recipient[:dashpos]+"@s.whatsapp.net"

        if message == 'hi':
            answer = "Hi "+namemitt+" " 

        elif message.startswith("hoi"):
            answer = "Bawak2 bersabor, "+namemitt+" "

        elif message == 'init 0':
            answer = "Ok "+namemitt+", shutting down. Bye bye."

        elif message == 'list command':
            answer = """List of command

  <system> <query>

System: NOVA or ICP

Query:
  *unbilled* - display number of unbilled account
  *progress* - current step of bill run
  *bainfo* <banumber> - BA Summary
"""

        else:
            a = WhatToFeedback()
            answer = a.getFeedback(message)

        if answer != "":
            print "sending to "+recipient+" : "+answer
 
            try:
                self.toLower(textmsg(answer, to = recipient))
            except Exception as e:
                print (e)
                print "unable to reply to "+recipient

