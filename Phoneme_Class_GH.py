def superflous_features(self, features, inclusive, exclusive):
    # this function zeros in on features that we know we need, and features that
    # are functionally identical, i.e. exclude the same phonemes. This will save our
    # algorithm from needing to do 10! operations.
    identicals = {}
    catalog = {}
    for feature in features:
        identicals[feature] = []
        catalog[feature] = []
    for feature in features:
        for excludable in exclusive:
            if getattr(inclusive[0], feature) != getattr(excludable, feature) and excludable not in catalog[feature]:
                catalog[feature].append(excludable)
                print("The feature %s excludes the phoneme %s" % (feature, excludable.name))
                # now we know all the phonemes that a feature excludes!
    for feature in features:
        comparative_value = catalog[feature]
        for otherFeature in features:
            if same_list(catalog[feature], catalog[otherFeature]) and otherFeature != feature:
                identicals[feature].append(otherFeature)
    return identicals
def populate_inclusive(sound_set):
    print("These are the special charactes for english consonants: ɹ ʤ ʧ ʒ ð θ ʃ ŋ ")
    print("These are the special characters for english vowels: ɑ æ ɔ ɪ ɛ ʊ ʌ ɒ ə" )
    inclusive= input("What Phonemes would you like to include? Type each one in seperated by a space.")
    inclusive= [a for a in inclusive if a != ' ']
    result = []
    for symbol in inclusive:
        for phoneme in sound_set:
            if phoneme.name == symbol:
               result.append(phoneme)
    return result
def populate_exclusive(sound_set):
    print("These are the special charactes for english consonants: ɹ ʤ ʧ ʒ ð θ ʃ ŋ ")
    print("These are the special characters for english vowels: ɑ æ ɔ ɪ ɛ ʊ ʌ ɒ ə" )
    exclusive= input("Now, What Phonemes would you like to Exclude? Type each one in seperated by a space.")
    exclusive= [a for a in exclusive if a != ' ']
    result = []
    for symbol in exclusive:
        for phoneme in sound_set:
            if phoneme.name == symbol:
               result.append(phoneme)
    return result

"""
def superflous_features(self, features, inclusive, exclusive):
    # this function zeros in on features that we know we need, and features that
    # are functionally identical, i.e. exclude the same phonemes. This will save our
    # algorithm from needing to do 10! operations.
    identicals = {}
    catalog = {}
    for feature in features:
        identicals[feature] = []
        catalog[feature] = []
    for feature in features:
        for excludable in exclusive:
            if getattr(inclusive[0], feature) != getattr(excludable, feature) and excludable not in catalog[feature]:
                catalog[feature].append(excludable)
                print("The feature %s excludes the phoneme %s" % (catalog[feature], excludable))
                # now we know all the phonemes that a feature excludes!
    for feature in features:
        comparative_value = catalog[feature]
        for otherFeature in features:
            if same_list(catalog[feature], catalog[otherFeature]) and otherFeature != feature:
                identicals[feature].append(otherFeature)
    return identicals"""


def same_list(first,second):
    # this function determines whether or not two lists are the same
    # regardless of the order of their elements.
    if len(first) != len(second):
        return False
    for a in first:
        if a not in second:
            return False
    for a in second:
        if a not in first:
            return False
    return True

def remove_clones(target_list):
    cloneless =[]
    for element in target_list:
        if element not in cloneless:
            cloneless.append(element)
    return cloneless
class combinable:
    def __init__(self,value_list):
        self.value_list= value_list

    def yield_all_combos(self):
        overcount = 0
        while overcount < len(self.value_list):
            for number in range(len(self.value_list[overcount])):
                holder = [a for a in self.value_list[overcount]]
                #print ("This is holder at first %s"%holder)
                if len(holder) > 1:
                    holder = holder[:number]+holder[(number+1):]
                    #print("now this is holder : %s"%holder)
                    self.value_list.append(holder)
                else:
                    pass
            overcount +=1
        self.value_list= remove_clones(self.value_list)




class phoneme:
    def __init__(self,name,consonantal,syllabic,sonorant,approximant,voice,spreadG,constrG,continuant,lateral,delR,nasal,
                 labial,round,coronal,anterior,distributed,strident,dorsal,high,low,front,back,atr):
        self.name = name
        self.consonantal = consonantal
        self.syllabic = syllabic
        self.sonorant = sonorant
        self.approximant = approximant
        self.voice = voice
        self.spreadG=spreadG
        self.constrG=constrG
        self.continuant = continuant
        self.lateral=lateral
        self.delR = delR
        self.nasal = nasal
        self.labial = labial
        self.round = round
        self.coronal = coronal
        self.anterior = anterior
        self.distributed = distributed
        self.strident = strident
        self.dorsal = dorsal
        self.high = high
        self.low = low
        self.front = front
        self.back = back
        self.atr = atr
    @staticmethod
    def necessary_features(features, inclusive, exclusive):
        result = {}
        catalog = {}
        for element in exclusive:
            catalog[element] = []
            for feature in features:
                if getattr(inclusive[0], feature) != getattr(element, feature) and feature not in catalog[element]:
                    catalog[element].append(feature)
                    print("The phoneme %s was excluded by the feature %s"%(element,feature))
        for key in catalog:
            print (catalog[key])
        for element in exclusive:
            if len(catalog[element]) == 1:
                result[element] = catalog[element][0]
                #print("the element %s can only be excluded by the feature %s" % (element.name, catalog[element][0]))
        return result
    def list_features(self):
        feature_list = [a for a in dir(self) if not a.startswith('__')]
        for element in feature_list:
            print(element +": " +str(getattr(self,element)))
    def find_contrast (self,otherPhoneme):
        resultList = []
        attrList = [a for a in dir(self) if not a.startswith('__')]
        for element in attrList:
            callAttr = getattr(self,element)
            paramAttr = getattr(otherPhoneme,element)
            if callAttr != paramAttr:
                resultList.append(element)
            else:
                pass
        print ("These are the features that are contrasting between \n the two sounds: "
               + str(resultList))
        return resultList
    @staticmethod
    def superflous_features(features, inclusive, exclusive):
        # this function zeros in on features that we know we need, and features that
        # are functionally identical, i.e. exclude the same phonemes. This will save our
        # algorithm from needing to do 10! operations.
        identicals = {}
        result = {}
        catalog = {}
        for feature in features:
            catalog[feature] = []
            identicals[feature] =[]
        for feature in features:
            for excludable in exclusive:
                if getattr(inclusive[0], feature) != getattr(excludable, feature) and excludable not in catalog[
                    feature]:
                    catalog[feature].append(excludable)
                    #print("The feature %s excludes the phoneme %s" % (feature, excludable.name))
                    # now we know all the phonemes that a feature excludes!
        already_done = []
        for feature in features:
            comparative_value = catalog[feature]
            for otherFeature in features:
                if same_list(catalog[feature], catalog[otherFeature]) and otherFeature != feature and feature not in already_done:
                    identicals[feature].append(otherFeature)
                    already_done.append(otherFeature)

            for key in identicals:
                if identicals[key] != []:
                    result[key] = identicals[key]
        return result

    @staticmethod
    def one_shot_wonders(features,inclusive,exclusive):
        # this method just tests if any one feature can singlehandedly do the job
        results = []
        for feature in features:
            test = True
            for excludable in exclusive:
                if getattr(inclusive[0],feature) == getattr(excludable,feature):
                    test = False
            if test == True:
                results.append(feature)
        return results

    @staticmethod
    def superordinate_features(features, inclusive, exclusive):
        # this function zeros in on features that are "objectively better" than other features
        # in the sense that one feature will exclude all of the phonemes another can, and more.
        superordinates = {}
        result = {}
        catalog = {}
        for feature in features:
            catalog[feature] = []
            superordinates[feature] = []
        for feature in features:
            for excludable in exclusive:
                if getattr(inclusive[0], feature) != getattr(excludable, feature) and excludable not in catalog[
                    feature]:
                    catalog[feature].append(excludable)
                    # print("The feature %s excludes the phoneme %s" % (feature, excludable.name))
                    # now we know all the phonemes that a feature excludes!

        # thank you stack overflow for this piece of code :) this sorts the dictionary so that the keys
        # with the most entries are up front - e.g. The features that exclude the most phonemes are first.
        descending_Order = sorted(catalog, key = lambda k : len(catalog[k]),reverse=True)

        subsumed = []
        for feature in descending_Order:
            for other_feature in catalog:
                if feature != other_feature and len(catalog[feature])> len (catalog[other_feature]) and feature not in subsumed:
                    tester = True
                    for element in catalog[other_feature]:
                        if element not in catalog[feature]:
                            tester = False
                    if tester == True:
                        superordinates[feature].append(other_feature)
                        subsumed.append(other_feature)

        # now to remove all null entries
        for key in superordinates:
            if superordinates[key] != []:
                result[key] = superordinates[key]
        return result


    @staticmethod
    def did_it_work(features,inclusive,exclusive):
        result = True
        got_excluded =[]
        for feature in features:
            for phoneme in exclusive:
                if getattr(inclusive[0],feature) != getattr(phoneme,feature) and phoneme not in got_excluded:
                    got_excluded.append(phoneme)
        for phoneme in exclusive:
            if phoneme not in got_excluded:
                result = False
        return result

    @staticmethod
    def print(phoneme_list):
        for phoneme in phoneme_list:
            print(phoneme.name)

    #################### end of Class Phoneme ##############################


### english consonant special characters  "ɹ ʤ ʧ ʒ ð θ ʃ ŋ"
### order of acquisition:

p = phoneme('p',True,False,False,False,False,False,False,False,False,False,False,True,False,False,
            None,True,False,False,None,None,None,None,None)
b = phoneme('b',True,False,False,False,True,False,False,False,False,False,False,True,False,False,
            None,True,False,False,None,None,None,None,None)
m = phoneme('m',True,False,True,False,True,False,False,False,False,False,True,True,False,False,
            None,True,False,False,None,None,None,None,None)
f = phoneme('f',True,False,False,False,False,False,False,True,False,True,False,True,False,False,
            None,False,True,False,None,None,None,None,None)
v = phoneme('v',True,False,False,False,True,False,False,True,False,True,False,True,False,False,
            None,True,True,False,None,None,None,None,None)
θ = phoneme ('θ',True,False,False,False,False,False,False,True,False,True,False,False,False,True,
                 True,True,False,False,None,None,None,None,None)
ð = phoneme ('ð',True,False,False,False,True,False,False,True,False,True,False,False,False,True,
                 True,True,False,False,None,None,None,None,None)
t = phoneme('t',True,False,False,False,False,False,False,False,False,False,False,False,False,True,True,False,False,False,
            None,None,None,None,None)
d = phoneme('d',True,False,False,False,True,False,False,False,False,False,False,False,False,True,True,False,False,False,
            None,None,None,None,None)
n = phoneme('n',True,False,True,False,True,False,False,False,False,False,True,False,False,True,True,False,False,False,
            None,None,None,None,None)
s = phoneme ('s',True,False,False,False,False,False,False,True,False,True,False,False,False,True,True,False,True,
             False,None,None,None,None,None)
z = phoneme ('z',True,False,False,False,True,False,False,True,False,True,False,False,False,True,True,False,True,
             False,None,None,None,None,None)
ɹ = phoneme ('ɹ',False,False,True,True,True,False,False,True,False,False,False,False,False,True,True,False,
             False,False,None,None,None,None,None)
l = phoneme ('l',True,False,True,True,True,False,False,True,True,False,False,False,False,True,True,False,
             False,False,None,None,None,None,None)
ʃ = phoneme ('ʃ',True,False,False,False,False,False,False,True,False,True,False,False,False,True,False,True,True,
             False,None,None,None,None,None)
ʒ = phoneme ('ʒ',True,False,False,False,True,False,False,True,False,True,False,False,False,True,False,True,True,
             False,None,None,None,None,None)
ʧ = phoneme ('ʧ',True,False,False,False,False,False,False,False,False,True,False,False,False,True,False,True,True,
             False,None,None,None,None,None)
ʤ = phoneme ('ʤ',True,False,False,False,True,False,False,False,False,True,False,False,False,True,False,True,True,
             False,None,None,None,None,None)
j= phoneme ('j',False,False,True,True,True,False,False,True,False,False,False,False,False,False,None,None,False,True,True,
            False,True,False,None)
w = phoneme ('w',False,False,True,True,True,False,False,True,False,False,False,True,True,False,None,None,
             False,True,True,False,False,True,None)
k = phoneme ('k',True,False,False,False,False,False,False,False,False,False,False,False,
             False,False,None,None,False,True,True,False,False,True,None)
g = phoneme ('g',True,False,False,False,True,False,False,False,False,False,False,False,
             False,False,None,None,False,True,True,False,False,True,None)
ŋ = phoneme ('ŋ',True,False,True,False,True,False,False,False,False,False,True,False,
             False,False,None,None,False,True,True,False,False,True,None)
h = phoneme ('h',False,False,False,False,False,True,False,True,False,True,False,False,False,False,None,None,False,False,None,None,None,None,None)



class Vowel(phoneme):
    def __init__(self,name,round,high,low,front,back,atr):
        self.name = name
        self.consonantal = False
        self.syllabic = True
        self.sonorant = True
        self.approximant = True
        self.voice = True
        self.spreadG= False
        self.constrG= False
        self.continuant = True
        self.lateral= False
        self.delR = False
        self.nasal = False
        self.labial = round
        self.round = round
        self.coronal = False
        self.anterior = None
        self.distributed = None
        self.strident = False
        self.dorsal = True
        self.high = high
        self.low = low
        self.front = front
        self.back = back
        self.atr = atr
## My friend told me to put these into a dictionary but I don't know if that's actually necessary or not
## my code probably won't work if the phonemes are put into this format of being in a dictionary TBH, so
## ignore this part.

#### special characters for english vowels  "ɑ æ ɔ ɪ ɛ ʊ ʌ ɒ"
#### order of acquisition = "round high low front back atr"

i = Vowel('i',False,True,False,True,False,True)
ɪ = Vowel('ɪ',False,True,False,True,False,False)
e = Vowel('e',False,False,False,True,False,True)
ɛ = Vowel ('ɛ',False,False,False,True,False,False)
æ = Vowel ('æ',False,False,True,True,False,True)
ə = Vowel ('ə',False,False,False,False,False,False)
a = Vowel ('a',False,False,True,False,False,False)
ʌ = Vowel ('ʌ',False,False,False,False,True,False)
u = Vowel ('u',True,True,False,False,True,True)
ʊ = Vowel ('ʊ',True,True,False,False,True,False)
o = Vowel ('o',True,False,False,False,True,True)
ɔ = Vowel ('ɔ',True,False,False,False,True,False)
ɑ = Vowel ('ɑ',False,False,True,False,True,False)
ɒ = Vowel ('ɒ',True,False,True,False,True,False)

### a list of all english phonemes:

english_phonemes = [a,e,i,o,u,ɑ,æ,ɔ,ɪ,ɛ,ʊ,ʌ,ɒ,ə,p,b,m,f,v,θ,ð,t,d,n,s,z,ɹ,l,ʃ,ʒ,ʧ,ʤ,j,w,k,g,ŋ,h]


def find_natural_class(inclusive,exclusive):
    alterable_exclusive = [a for a in exclusive]
    attributes = [a for a in dir(inclusive[0])if not a.startswith('__')]
    commonalities =[]
    overCommonalities=[]
    differences = []
    extras = []
    annoying_stuff = ['find_contrast','list_features']
    similars = {}
    null_givers =[]
    superordinates = {}
    # Step one; add up all the things the inclusive have in common.
    for element in attributes:
        addOrNot = True
        value = getattr(inclusive[0],element)
        for phoneme in inclusive:
            if getattr(phoneme,element) != value:
                addOrNot=False
        if addOrNot == True:
            commonalities.append(element)
        elif addOrNot==False:
            differences.append(element)

    # first off, we need to see if the user even tried to exclude anything

    if exclusive == []:
        print("The phonemes have the following common features")
        for feature in commonalities:
            sign = ''
            if getattr(inclusive[0], feature) == True:
                sign = ' + '
                print(sign + feature)
            elif getattr(inclusive[0], feature) == False:
                sign = ' - '
                print(sign + feature)
            elif getattr(inclusive[0], feature) == None:
                sign = ' null '
                print(sign + feature)
            else:
                pass
        return True

    # this is step two. getting rid of the extra features.
    # This will add the feature to overCommonalities unless it excludes
    # at least one phoneme in the exclusive list.
    for element in commonalities:
        removeOrNot = True
        value = getattr(inclusive[0],element)
        for phoneme in exclusive:
            if getattr(phoneme,element) != value:
                removeOrNot = False
        if removeOrNot==True:
            overCommonalities.append(element)
        else:
            pass
    commonalities = [a for a in commonalities if not a in overCommonalities]
    # Now, just make sure any annoying method names don't show up
    commonalities = [a for a in commonalities if not a in annoying_stuff]

    # We know we can remove the tonguerootpositionfeatures if the inclusive phonemes aren't dorsal.
    if 'dorsal' in commonalities and getattr(inclusive[0],'dorsal')== False:
        commonalities.remove('high')
        commonalities.remove('low')
        commonalities.remove('front')
        commonalities.remove('back')
       # commonalities.remove('atr')
    # the same goes for anteriorhood.
    if 'coronal' in commonalities and getattr(inclusive[0],'coronal')==False:
        commonalities.remove('anterior')

    # preprocessing's last stage. If a phoneme has a null value for a particular feature,
    # you just can't use it to help define the class. So let's get rid of it!
    for feature in commonalities:
        if getattr(inclusive[0],feature)== None:
            null_givers.append(feature)
    commonalities = [a for a in commonalities if a not in null_givers]

    print("The relevant features are: %s"%(commonalities))

################################### end of forebeworking ########################################



    # first, we need to see if making a natural class even works!

    if phoneme.did_it_work(commonalities,inclusive,exclusive) == False:
        print ("Unfortunately, a natural class cannot be made")
        return False


    one_shot_wonders = phoneme.one_shot_wonders(commonalities,inclusive,exclusive)
    correctAnswers = []
    shortestCorrectAnswers = []




    if len(one_shot_wonders) == 0:
        # if none of the features can do it on their own, then there is
        # more attenuation to do! Let's focus on what we KNOW that we need to do.
        necessaries= phoneme.necessary_features(commonalities,inclusive,exclusive)
        needed_features = []
        #phonemes that would be ruled out by those necessary features.
        discounted_phonemes =[]
        for key in necessaries:
            discounted_phonemes.append(key)
            needed_features.append(necessaries[key])
        commonalities = [feature for feature in commonalities if feature not in needed_features]
        alterable_exclusive = [phoneme for phoneme in alterable_exclusive if phoneme not in discounted_phonemes]
        # the point of this alterable exclusive variable, is that all of the remaining features
        # (the ones besides the uniquely necessary ones) only need to be able to exclude the phonemes that
        # the necessary ones were unable to exclude.

        print("it made it this far!")
        print (commonalities)



        # Now to find out if any features are functionally similar.
        similars = phoneme.superflous_features(commonalities,inclusive,alterable_exclusive)
        for key in similars:
            for element in key:
                extras.append(element)
        commonalities = [a for a in commonalities if a not in extras]


        # now to pick out any superordinate features

        superordinates= phoneme.superordinate_features(commonalities,inclusive,alterable_exclusive)
        subordinates = []
        for key in superordinates:
            for element in key:
                subordinates.append(element)
        commonalities = [a for a in commonalities if a not in subordinates]



        # now to combine all the possibilities :)
        Combo = combinable([commonalities])
        Combo.yield_all_combos()
        #for thing in Combo.value_list:
         #   print (thing)
        # now to test if each combination does the trick at excluding all of the phonemes we wanted.

        for ncDefinition in Combo.value_list:
            gotExcluded = []
            for feature in ncDefinition:
                for excludable in alterable_exclusive:
                    if getattr(inclusive[0],feature)!= getattr(excludable,feature) and excludable not in gotExcluded:
                        gotExcluded.append(excludable)
            did_it_work = True
            for phoneme in alterable_exclusive:
                if phoneme not in gotExcluded:
                    did_it_work = False
                else:
                    pass
            if did_it_work == True:
                correctAnswers.append(ncDefinition)
        # Now that we haev all of the correct answers, we need to see which of them are the shortest.
        # Let's first determine how long the most parsimonious answer(s) is/are.
        minLength = len(correctAnswers[0])
        for ncDefinition in correctAnswers:
            if len(ncDefinition) < minLength:
                minLength = len(ncDefinition)
        # all ncDefinitions of equal length will be considered "correct answers."
        shortestCorrectAnswers = []
        for answer in correctAnswers:
            if len(answer) == minLength:
                shortestCorrectAnswers.append(answer)
        # now to re-add the necessary features :)
        # !!!Important note, now that we've readded the important features, we want to test everything
        # on the exclusive list, not the alterable_exclusive list. But while these features were gone,
        # we wanted to try things out on the alterable_exclusive list.
        for answer in shortestCorrectAnswers:
            for feature in needed_features:
                answer.append(feature)
                print("Appending this necessary feature on: %s"%(feature) )
    elif len(one_shot_wonders) > 0:
        for element in one_shot_wonders:
            shortestCorrectAnswers.append([element])

    # now to see if any subordinates can be readded in
    for key in superordinates:
        for answer in shortestCorrectAnswers:
            if key in answer:
                for underordinate in key:
                    temp_copy = [a for a in answer]
                    temp_copy[temp_copy.index(key)]=underordinate
                    if phoneme.did_it_work(temp_copy,inclusive,exclusive):
                        shortestCorrectAnswers.append(temp_copy)

    # now to readd in any extras that were "functionally similar" features
    for key in similars:
        for answer in shortestCorrectAnswers:
            if key in answer:
                for substitution in key:
                    temp_copy = [a for a in answer]
                    temp_copy[temp_copy.index(key)]=substitution
                    shortestCorrectAnswers.append(temp_copy)

    # now to print out the answer in a way that is easy on the eyes.
    answerOverCount=0
    for answer in shortestCorrectAnswers:
        answerString = ""
        for feature in answer:
            plusOrMinus= ""
            if getattr(inclusive[0],feature) == True:
                plusOrMinus =" + "
            elif getattr(inclusive[0],feature) == False:
                plusOrMinus=" - "
            answerString += plusOrMinus
            answerString += feature
        answerOverCount += 1
        print ("Answer number %s is: \n"%(answerOverCount) +answerString)
        # it might be a good idea to also return the least parsimonious answer.



#### special characters for english vowels  "ɑ æ ɔ ɪ ɛ ʊ ʌ ɒ ə"
### english consonant special characters  "ɹ ʤ ʧ ʒ ð θ ʃ ŋ"


inclusive = populate_inclusive(english_phonemes)
exclusive = populate_exclusive(english_phonemes)

find_natural_class(inclusive,exclusive)


print ("write exit when you are done")
exit = ''
while exit != 'exit':
    exit= input("Do you want to quit? if so, write exit (no caps, or spaces)")

