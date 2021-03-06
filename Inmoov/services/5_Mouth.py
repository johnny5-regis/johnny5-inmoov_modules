# -- coding: utf-8 --
# ##############################################################################
#                 MOUTH SERVICE FILE
# ##############################################################################


# ##############################################################################
# MRL SERVICE CALL
# ##############################################################################

global VoiceError
VoiceError=0
try:
  #subconsciousMouth is an always worky english voice used to diagnostic
  #inmoov mouth service
  i01.mouth = Runtime.createAndStart("i01.mouth", MyvoiceTTS)
  mouth=i01.mouth
  #mouth.speak(",")
  
except:
  mouth=subconsciousMouth
  errorSpokenFunc('MyvoiceType')
  VoiceError=1
  pass


#vocal startup globalized so :
i01.setMute(1)

python.subscribe(mouth.getName(),"publishStartSpeaking")
python.subscribe(mouth.getName(),"publishEndSpeaking")

# ##############################################################################
# MRL SERVICE TWEAKS
# ##############################################################################
global lastValue
lastValue=0
#analog pin listener use 
def publishMouthcontrolPinLeft(pins):
  global AudioInputValues
  global AudioInputRawValue

  for pin in range(0, len(pins)):
    #print pins[pin].value
    #mouth control listener
    if isHeadActivated:
      if AudioSignalProcessingCalibration:AudioInputValues.append(pins[pin].value)
        
      if AudioSignalProcessing:
        if pins[pin].value>minAudioValue:
          head.jaw.setVelocity(random.uniform(200,500))
          if not head.jaw.isMoving():head.jaw.moveTo(int(pins[pin].value))
    

#functions to call about robot speak
def talk(data):
  if data:
    data=unicode(data,'utf-8')
    if data[0:2].lower()=="l ":data=data.replace("l ", "l'")
    if data[0:2].lower()=="j ":data=data.replace("j ", "j'")
    if data[0:2].lower()=="c ":data=data.replace("c ", "c'")
    if data[0:2].lower()=="d ":data=data.replace("d ", "d'")
    data=data.lower().replace(" j ", " j'")
    data=data.lower().replace(" l ", " l'")
    data=data.lower().replace(" c ", " c'")
    data=data.lower().replace(" d ", " d'")
    data=data.lower().replace("it s", "it's")
    mouth.speak(data)
    
def talkBlocking(data):
  if data:
    data=unicode(data,'utf-8')
    if data[0:2].lower()=="l ":data=data.replace("l ", "l'")
    if data[0:2].lower()=="j ":data=data.replace("j ", "j'")
    if data[0:2].lower()=="c ":data=data.replace("c ", "c'")
    if data[0:2].lower()=="d ":data=data.replace("d ", "d'")
    data=data.lower().replace(" j ", " j'")
    data=data.lower().replace(" l ", " l'")
    data=data.lower().replace(" c ", " c'")
    data=data.lower().replace(" d ", " d'")
    data=data.lower().replace("it s", "it's")
    data=data.replace(" j ", " j'")
    data=data.replace(" l ", " l'")
    mouth.speakBlocking(data)
    
def talkEvent(data):
  if IsMute==0:
    data=unicode(data,'utf-8')
    subconsciousMouth.speakBlocking(data)

#stop autolisten
def onEndSpeaking(text):

  if i01.RobotIsStarted:
    
    if not MoveRandomTimer.isClockRunning:
      MoveHeadTimer.stopClock()
      MoveEyesTimer.stopClock()
    if flash_when_speak and isNeopixelActivated:i01.stopNeopixelAnimation()

  if AudioSignalProcessing:
    try:
      left.disablePin(AnalogPinFromSoundCard)
      head.jaw.setVelocity(100)
      head.jaw.moveTo(0)
      #head.jaw.setVelocity(200)
      #head.jaw.moveTo(0)
    except:
      print "onEndSpeaking error"
      pass
  
def onStartSpeaking(text):
  
  if AudioSignalProcessing:
    try:left.enablePin(AnalogPinFromSoundCard,HowManyPollsBySecond)      
    except:
      print "onStartSpeaking error"
      pass
  if i01.RobotIsStarted:

    if 'oui ' in text or 'yes ' in text or ' oui' in text or 'ja ' in text or text=="yes" or text=="oui":Yes()
    if 'non ' in text or 'no ' in text or 'nicht ' in text or 'neen ' in text or text=="no" or text=="non":No()

    #force random move while speaking, to avoid conflict with random life gesture
    if random.randint(0,1)==1:
      i01.RobotCanMoveHeadRandom=True
      MoveHeadTimer.startClock()
    if random.randint(0,1)==1:
      i01.RobotCanMoveEyesRandom=True
      MoveEyesTimer.startClock()
    if flash_when_speak and isNeopixelActivated:i01.setNeopixelAnimation("Flash Random", 255, 255, 255, 1)
    
# ##############################################################################
# MOUTH RELATED FUNCTIONS
# ##############################################################################

#to know what is marytts version
def getMaryttsVersion():
  try:
    versionMary="5.2"
  except:
    versionMary=0
    pass
  return versionMary
  
#to check if marytts voice exist
def CheckMaryTTSVoice(voiceCheck):
  return os.access(os.getcwd().replace("\\", "/")+'/libraries/jar/voice-'+voiceCheck+'-'+getMaryttsVersion()+'.jar', os.R_OK)

#mouth functions
def setRobotLanguage():
  global LanguageError
  LanguageError=0
  tmplanguage=MyLanguage
  if MyvoiceTTS=="VoiceRss" or MyvoiceTTS=="Polly":
    if tmplanguage=="fr":tmplanguage="fr-fr"
    if tmplanguage=="en":tmplanguage="en-us"
    if tmplanguage=="es":tmplanguage="es-es"
    if tmplanguage=="de":tmplanguage="de-de"
    if tmplanguage=="nl":tmplanguage="nl-nl"
    if tmplanguage=="ru":tmplanguage="ru-ru"
  
  try:
    if MyvoiceTTS=="VoiceRss":i01.mouth.setKey(VoiceRssApi)
  except:
    pass
    
  try:  
    if MyvoiceTTS=="Polly":i01.mouth.setKey(awsaccesskeyid,awssecretkey)
  except:
    pass
    
  try:  
    if MyvoiceTTS=="IndianTts":
      i01.mouth.api=IndianTtsApi
      i01.mouth.userid=IndianTtsUserId
  except:
    pass

  
  try:
    mouth.setLanguage(tmplanguage)
    if EarEngine=="WebkitSpeechRecognition":i01.ear.setLanguage(MyLanguage)
  except:
    errorSpokenFunc('MyLanguage')
    LanguageError=1
    pass
  
      
def checkAndDownloadVoice():        
  if MyvoiceTTS=="MarySpeech":
    if not CheckMaryTTSVoice(MyvoiceType):
      try:
        mouth.installComponentsAcceptLicense(MyvoiceType)
      except:
        pass
      if os.access(os.getcwd().replace("\\", "/")+'/libraries/jar/voice-'+MyvoiceType+'-'+getMaryttsVersion()+'.jar', os.R_OK):
        errorSpokenFunc('VoiceDownloaded')
        sleep(4)
        runtime.restart()
      else:
        errorSpokenFunc('I_cannot_download_this_mary_T_T_S_voice',MyvoiceType)
        
    
def setCustomVoice():  
  global VoiceError
  VoiceError=0
  try:
    mouth.setVoice(unicode(MyvoiceType,'utf-8'))
  except:
    errorSpokenFunc('MyvoiceType')
    VoiceError=1
    pass
    
#we start raw Inmoov ear and mouth service
i01.startMouth()
#set user language

setRobotLanguage()

#check and update marytts voices  
#no worky on linux
if not IuseLinux:
  checkAndDownloadVoice()
#set CustomVoice
setCustomVoice()
#set english subconsious mouth to user globalised mouth now ( only if we found a language pack )


try:
  mouth.speak(",")
except:
  errorSpokenFunc('lang_VoiceRssNoWorky')
  VoiceError=1
  mouth=subconsciousMouth
  pass

if languagePackLoaded==1 and LanguageError==0 and VoiceError==0:
  subconsciousMouth=mouth
if languagePackLoaded==0:
  errorSpokenFunc('BadLanguagePack')


talkEvent(lang_whatIsThisLanguage)
talkEvent(lang_startingEar+", "+EarEngine)