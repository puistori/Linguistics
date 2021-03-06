import sys
from PyQt5 import QtWidgets, QtGui, Qt
from PyQt5.QtWidgets import QComboBox, QMessageBox, QMenuBar, QMainWindow, QApplication, QAction, qApp, QMdiArea, \
    QTableWidget, QTableWidgetItem , QTextEdit , QCheckBox,QInputDialog,QFrame,QSizePolicy,QSpacerItem
from PyQt5.QtGui import QIcon, QPixmap
import re
from threading import Timer
import pickle
from PyQt5.QtCore import QObject,pyqtSignal,pyqtSlot
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math
from functools import partial
from PyQt5 import QtCore
import os
from tkinter import *
from tkinter import filedialog

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
                # now we know all the phonemes that a feature excludes!
    for feature in features:
        comparative_value = catalog[feature]
        for otherFeature in features:
            if same_list(catalog[feature], catalog[otherFeature]) and otherFeature != feature:
                identicals[feature].append(otherFeature)
    return identicals


# The populate functions are only needed for when the program runs directly out of the command prompt.
def populate_inclusive(sound_set):
    
    
    inclusive = input("What Phonemes would you like to include? Type each one in seperated by a space.")
    inclusive = [a for a in inclusive if a != ' ']
    result = []
    for symbol in inclusive:
        for phoneme in sound_set:
            if phoneme.name == symbol:
                result.append(phoneme)
    return result


def populate_exclusive(sound_set):
    
    
    exclusive = input("Now, What Phonemes would you like to Exclude? Type each one in seperated by a space.")
    exclusive = [a for a in exclusive if a != ' ']
    result = []
    for symbol in exclusive:
        for phoneme in sound_set:
            if phoneme.name == symbol:
                result.append(phoneme)
    return result


def same_list(first, second):
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
    cloneless = []
    for element in target_list:
        if element not in cloneless:
            cloneless.append(element)
    return cloneless


class combinable:
    def __init__(self, value_list):
        self.value_list = value_list

    def yield_all_combos(self):
        overcount = 0
        while overcount < len(self.value_list):
            for number in range(len(self.value_list[overcount])):
                holder = [a for a in self.value_list[overcount]]
                if len(holder) > 1:
                    holder = holder[:number] + holder[(number + 1):]
                    self.value_list.append(holder)
                else:
                    pass
            overcount += 1
        self.value_list = remove_clones(self.value_list)


class phoneme:

    @staticmethod
    def necessary_features(features, inclusive, exclusive):
        result = {}
        catalog = {}
        for element in exclusive:
            catalog[element] = []
            for feature in features:
                if getattr(inclusive[0], feature) != getattr(element, feature) and feature not in catalog[element]:
                    catalog[element].append(feature)
        for key in catalog:
            
            pass
        for element in exclusive:
            if len(catalog[element]) == 1:
                result[element] = catalog[element][0]
        return result

    def list_features(self):
        feature_list = [a for a in dir(self) if not a.startswith('__')]
        for element in feature_list:
            pass
            
    def find_contrast(self, otherPhoneme):
        resultList = []
        attrList = [a for a in dir(self) if not a.startswith('__')]
        for element in attrList:
            callAttr = getattr(self, element)
            paramAttr = getattr(otherPhoneme, element)
            if callAttr != paramAttr:
                resultList.append(element)
            else:
                pass
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
            identicals[feature] = []
        for feature in features:
            for excludable in exclusive:
                if getattr(inclusive[0], feature) != getattr(excludable, feature) and excludable not in catalog[
                    feature]:
                    catalog[feature].append(excludable)
        already_done = []
        for feature in features:
            comparative_value = catalog[feature]
            for otherFeature in features:
                if same_list(catalog[feature],
                             catalog[otherFeature]) and otherFeature != feature and feature not in already_done:
                    identicals[feature].append(otherFeature)
                    already_done.append(otherFeature)

            for key in identicals:
                if identicals[key] != []:
                    result[key] = identicals[key]
        return result

    @staticmethod
    def one_shot_wonders(features, inclusive, exclusive):
        # this method just tests if any one feature can singlehandedly do the job
        results = []
        for feature in features:
            test = True
            for excludable in exclusive:
                if getattr(inclusive[0], feature) == getattr(excludable, feature):
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

        # thank you stack overflow for this piece of code :) this sorts the dictionary so that the keys
        # with the most entries are up front - e.g. The features that exclude the most phonemes are first.
        descending_Order = sorted(catalog, key=lambda k: len(catalog[k]), reverse=True)

        subsumed = []
        for feature in descending_Order:
            for other_feature in catalog:
                if feature != other_feature and len(catalog[feature]) > len(
                        catalog[other_feature]) and feature not in subsumed:
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
    def did_it_work(features, inclusive, exclusive):
        result = True
        got_excluded = []
        for feature in features:
            for phoneme in exclusive:
                if getattr(inclusive[0], feature) != getattr(phoneme, feature) and phoneme not in got_excluded:
                    got_excluded.append(phoneme)
        for phoneme in exclusive:
            if phoneme not in got_excluded:
                result = False
        return result

    @staticmethod
    def print_phoneme_list(phoneme_list):
        for phoneme in phoneme_list:
            pass
    #################### end of Class Phoneme ##############################


def find_natural_class(inclusive, exclusive,display_window,feature_set,inventory):
    # I think this needs to be filled with actual phonemes. so set map was better
    ambient_inventory = set_map[feature_set][inventory]
    alterable_exclusive = [a for a in exclusive]
    attributes = [a for a in dir(inclusive[0]) if not a.startswith('__')]
    commonalities = []
    overCommonalities = []
    differences = []
    extras = []
    annoying_stuff = ['find_contrast', 'list_features','name']
    similars = {}
    null_givers = []
    superordinates = {}
    inclusive_display = ""

    if len(inclusive) == 1:
        inclusive_display= (" %s and only %s."%(inclusive[0].name,inclusive[0].name))
    else:
        for number in range(len(inclusive)-1):
            inclusive_display+= ' '
            inclusive_display += inclusive[number].name
            inclusive_display += ','
        inclusive_display += " and %s,"%(inclusive[len(inclusive)-1].name)
    exclusive_display = ""
    if len(exclusive)== 0:
        exclusive_display = " nothing at all"
    elif len(exclusive) == 1:
        exclusive_display= (" %s and only %s."%(exclusive[0].name,exclusive[0].name))
    else:
        for number in range(len(exclusive)-1):
            exclusive_display+= ' '
            exclusive_display += exclusive[number].name
            exclusive_display += ','
        exclusive_display += " and %s"%(exclusive[len(exclusive)-1].name)
    display_window.append("Featureset: %s"%feature_set)
    display_window.append("Phoneme Inventory: %s"%inventory)
    display_window.append("You have opted to include the phonemes %s while excluding %s"%(inclusive_display,exclusive_display))
    display_window.setWindowTitle("Answer for including %s while excluding %s"%(inclusive_display[:len(inclusive_display)-1],exclusive_display))
    display_window.setWindowIcon(QtGui.QIcon('pictures/main logo.png'))
    # Step one; add up all the things the inclusive have in common.
    for element in attributes:
        addOrNot = True
        value = getattr(inclusive[0], element)
        for phoneme in inclusive:
            if getattr(phoneme, element) != value:
                addOrNot = False
        if addOrNot == True:
            commonalities.append(element)
        elif addOrNot == False:
            differences.append(element)

    # first off, we need to see if the user even tried to exclude anything

    if exclusive == []:
        display_window.append("The phonemes have the following common features:")
        for feature in commonalities:
            sign = ''
            if getattr(inclusive[0], feature) == True:
                sign = ' + '
                display_window.append((sign + feature))
            elif getattr(inclusive[0], feature) == False:
                sign = ' - '
                display_window.append((sign + feature))
            elif getattr(inclusive[0], feature) == None:
                sign = ' null '
                display_window.append((sign + feature))
            else:
                pass
        window_height = 50 + 17*len(commonalities)
        display_window.setGeometry(200,200,400,window_height)
        return True

    # this is step two. getting rid of the extra features.
    # This will add the feature to overCommonalities unless it excludes
    # at least one phoneme in the exclusive list.
    for element in commonalities:
        removeOrNot = True
        value = getattr(inclusive[0], element)
        for phoneme in exclusive:
            if getattr(phoneme, element) != value:
                removeOrNot = False
        if removeOrNot == True:
            overCommonalities.append(element)
        else:
            pass
    commonalities = [a for a in commonalities if not a in overCommonalities]
    # Now, just make sure any annoying method names don't show up
    commonalities = [a for a in commonalities if not a in annoying_stuff]

    # We know we can remove the tonguerootpositionfeatures if the inclusive phonemes aren't dorsal.
    if 'dorsal' in commonalities and getattr(inclusive[0], 'dorsal') == False:
        commonalities.remove('high')
        commonalities.remove('low')
        commonalities.remove('front')
        commonalities.remove('back')
    # commonalities.remove('atr')
    # the same goes for anteriorhood.
    if 'coronal' in commonalities and getattr(inclusive[0], 'coronal') == False:
        commonalities.remove('anterior')

    # preprocessing's last stage. If a phoneme has a null value for a particular feature,
    # you just can't use it to help define the class. So let's get rid of it!
    for feature in commonalities:
        if getattr(inclusive[0], feature) == None:
            null_givers.append(feature)
    commonalities = [a for a in commonalities if a not in null_givers]

    display_window.append("The relevant features are: %s" % (commonalities))

    ################################### end of forebeworking ########################################

    # first, we need to see if making a natural class even works!

    if phoneme.did_it_work(commonalities, inclusive, exclusive) == False:
        display_window.append("Unfortunately, a natural class cannot be made")
        return False

    one_shot_wonders = phoneme.one_shot_wonders(commonalities, inclusive, exclusive)
    correctAnswers = []
    shortestCorrectAnswers = []

    if len(one_shot_wonders) == 0:
        # if none of the features can do it on their own, then there is
        # more attenuation to do! Let's focus on what we KNOW that we need to do.
        necessaries = phoneme.necessary_features(commonalities, inclusive, exclusive)
        needed_features = []
        # phonemes that would be ruled out by those necessary features.
        discounted_phonemes = []
        for key in necessaries:
            discounted_phonemes.append(key)
            if necessaries[key] not in needed_features:
                needed_features.append(necessaries[key])
        commonalities = [feature for feature in commonalities if feature not in needed_features]
        alterable_exclusive = [phoneme for phoneme in alterable_exclusive if phoneme not in discounted_phonemes]
        # the point of this alterable exclusive variable, is that all of the remaining features
        # (the ones besides the uniquely necessary ones) only need to be able to exclude the phonemes that
        # the necessary ones were unable to exclude.


        # Now to find out if any features are functionally similar.
        similars = phoneme.superflous_features(commonalities, inclusive, alterable_exclusive)
        for key in similars:
            for element in similars[key]:
                extras.append(element)
        commonalities = [a for a in commonalities if a not in extras]

        # now to pick out any superordinate features

        superordinates = phoneme.superordinate_features(commonalities, inclusive, alterable_exclusive)
        subordinates = []
        for key in superordinates:
            for element in key:
                subordinates.append(element)
        commonalities = [a for a in commonalities if a not in subordinates]

        # now to combine all the possibilities :)
        Combo = combinable([commonalities])
        Combo.yield_all_combos()
        # for thing in Combo.value_list:
        #   print (thing)
        # now to test if each combination does the trick at excluding all of the phonemes we wanted.

        for ncDefinition in Combo.value_list:
            gotExcluded = []
            for feature in ncDefinition:
                for excludable in alterable_exclusive:
                    if getattr(inclusive[0], feature) != getattr(excludable, feature) and excludable not in gotExcluded:
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
    elif len(one_shot_wonders) > 0:
        for element in one_shot_wonders:
            shortestCorrectAnswers.append([element])

    # now to see if any subordinates can be readded in
    for key in superordinates:
        for answer in shortestCorrectAnswers:
            if key in answer:
                for underordinate in superordinates[key]:
                    temp_copy = [a for a in answer]
                    temp_copy[temp_copy.index(key)] = underordinate
                    if phoneme.did_it_work(temp_copy, inclusive, exclusive):
                        shortestCorrectAnswers.append(temp_copy)

    # now to readd in any extras that were "functionally similar" features
    for key in similars:
        for answer in shortestCorrectAnswers:
            if key in answer:
                for substitution in similars[key]:
                    temp_copy = [a for a in answer]
                    temp_copy[temp_copy.index(key)] = substitution
                    shortestCorrectAnswers.append(temp_copy)

    # now to print out the answer in a way that is easy on the eyes.
    answerOverCount = 0
    for answer in shortestCorrectAnswers:
        answerString = ""
        for feature in answer:
            plusOrMinus = ""
            if getattr(inclusive[0], feature) == True:
                plusOrMinus = " + "
            elif getattr(inclusive[0], feature) == False:
                plusOrMinus = " - "
            answerString += plusOrMinus
            answerString += feature
        answerOverCount += 1

        ### Here, I am entering code that will make it so that the program will also tell you what other phonemes
        ### are included with each answer.
        other_phonemes = []
        for phoneme in ambient_inventory:
            add_me = True
            for feature in answer:
                if getattr(phoneme,feature) != getattr(inclusive[0],feature):
                    add_me = False
            if add_me == True:
                other_phonemes.append(phoneme.name)
        if len(other_phonemes) > 0:
            others_included = "\n This answer will form a group including the following phonemes: "
            for phoneme_name in other_phonemes:
                others_included += phoneme_name
                others_included += ", "
        ## this next elif statement is actually useless in this code. I was thinking maybe I have the program
        ## report what OTHER phonemes are included, but it might be better to just say which phonemes are included
        ## including the ones we put on the including list. idk. 
        elif len(other_phonemes) == 0:
            others_included = "\n No other phonemes will be included by this answer."




        display_window.append("Answer number %s is: \n" % (answerOverCount) + answerString + others_included)
        window_height = 75 + (34*answerOverCount)
        display_window.setGeometry(200,200,750,window_height)
        # it might be a good idea to also return the least parsimonious answer.

def class_creator(name, attributes):
    new_attr = ['name']
    for element in attributes:
        new_attr.append(element)
    def new_init(self,**kwargs):
        self.attributes = [a for a in new_attr]
        specified_attributes = []
        for key,value in kwargs.items():
            if key in self.attributes:
                self.__setattr__(key,value)
                specified_attributes.append(key)
            elif key not in self.attributes:
                raise TypeError("Sorry, the argument %s doesn't work here"%key)
        unspecified_attributes = [a for a in self.attributes if a not in specified_attributes]
        for unsp_attribute in unspecified_attributes:
            self.__setattr__(unsp_attribute,None)
    new_class = type(name,(phoneme,),{"__init__":new_init})
    return new_class


#################################3 setup

"""

## this is actually going to get pickled
feature_set_map = {'bakovicean_phoneme':['consonantal','syllabic','sonorant','approximant','voice','spreadG','constrG','continuant',
                                                          'lateral','delR','nasal','labial','round','coronal','anterior','distributed','strident',
                                                          'dorsal','high','low','front','back','atr']}



phoneme_map ={}

#bakovichean_phoneme = class_creator('bakovicean_phoneme',['consonantal','syllabic','sonorant','approximant','voice','spreadG','constrG','continuant',
#                                                          'lateral','delR','nasal','labial','round','coronal','anterior','distributed','strident',
#                                                          'dorsal','high','low','front','back','atr'])
dictionish = {'bakovicean_phoneme':[(('name','p'),('consonantal',True),('syllabic',False),('sonorant',False),('approximant',False),('voice',False),('spreadG',False),('constrG',False),
              ('continuant',False),('lateral',False),('delR',False),('nasal',False),('labial',True),('round',False),('coronal',False),('anterior',None),('distributed',True),
              ('strident',False),('dorsal',False),('high',None),('low',None),('front',None),('back',None),('atr',None))]}

inventories ={'bakovicean_phoneme':{'All Phonemes':['p'],'English':['p']}}

new_phoneme_map = {}

set_map = {"bakovicean_phoneme":{"All Phonemes":[],"English":[]}}
"""
"""
p = bakovichean_phoneme(name='p',consonantal=True,syllabic = False, sonorant = False, approximant= False,voice = False, spreadG = False, constrG = False,
                        continuant = False, lateral = False, delR = False, nasal = False, labial = True, round = False, coronal = False, anterior = None,
                        distributed = True, strident= False, dorsal = False, high = None, low = None, front = None, back = None, atr = None)
b = bakovichean_phoneme(name='b',consonantal=True,syllabic = False, sonorant = False, approximant= False,voice = True, spreadG = False, constrG = False,
                        continuant = False, lateral = False, delR = False, nasal = False, labial = True, round = False, coronal = False, anterior = None,
                        distributed = True, strident= False, dorsal = False, high = None, low = None, front = None, back = None, atr = None)

t = bakovichean_phoneme(name='t')

"""


#### pickling in ####

try:
    pickle_in = open("feature_set_map","rb")
    feature_set_map = pickle.load(pickle_in)
    pickle_in = open("dictionish","rb")
    dictionish = pickle.load(pickle_in)
    pickle_in = open("inventories","rb")
    inventories = pickle.load(pickle_in)
    pickle_in = open("technical_map","rb")
    technical_map = pickle.load(pickle_in)
    
    feature_set_class_map= {}
    set_map = {}
    phoneme_map = {}
except Exception as e:
    
    feature_set_map = {}
    dictionish = {}
    inventories = {}
    technical_map = {}
    phoneme_map = {}
    set_map = {}
    feature_set_class_map = {}
#
#




shiftereens = {'name': 'akbar', 'long': True, 'consonantal': None, 'syllabic': None, 'sonorant': None, 'approximant': None,
 'voice': None, 'spreadg': None, 'constrg': None, 'continuant': None, 'lateral': None, 'delr': None, 'nasal': None,
 'labial': None, 'round': None, 'coronal': None, 'anterior': None, 'distributed': None, 'strident': None, 'dorsal': None,
 'high': None, 'low': None, 'front': None, 'back': None, 'atr': None}

#keski = feature_set_class_map['with_long'](**shiftereens)
#
"""
kraelan = {'name':'zerpilan','test':True,'testing':False,'testful':None}

feature_set_class_map['test'] = class_creator('test',['test','testing','testful'])
zerp = feature_set_class_map['test'](name='zerpiboof',test=True,testing=False,testful=None)
zorpi = feature_set_class_map['test'](**{'name':'zerpilan','test':True,'testing':False,'testful':None})

print (zorpi.name)
print (zorpi.test)
print (zorpi.attributes)




"""

## just for the record, set map is useful for the inspect widget when you are populating the table.
## It enables you to quickly go from a phoneme name that is in an inventory, to an actual phoneme object that has the properties.
# The set map also is useful in the main function, when you need to access the phonemes themselves , not just their names (like the ambient inventory variable)
## phoneme map is similar, and is useful for the assign phoneme function. The phoneme map allows you to quickly go from a phoneme's name to the phoneme itself.
def generate_phonemes(stored_data, feature_set):
    for key in feature_set_map:
        feature_set_class_map[key] = class_creator(key, feature_set_map[key])
    global phoneme_map
    phoneme_map[feature_set] = {}
    set_map[feature_set] = {}
    
    
    
    phonemes_list = stored_data[feature_set]
    global inventories
    for inventory in inventories[feature_set]:
        set_map[feature_set][inventory] = []
    
    for phoneme in phonemes_list:
        kwargsDict = {}
        for attribute in phoneme:
            kwargsDict[attribute[0]] = attribute[1]
        new_phoneme = feature_set_class_map[feature_set](**kwargsDict)
        
        #
        #
        #
        #print (kwargsDict)
        for inventory in inventories[feature_set]:
            if new_phoneme.name in inventories[feature_set][inventory]:
                #
                set_map[feature_set][inventory].append(new_phoneme)
        phoneme_map[feature_set][new_phoneme.name]=new_phoneme
        



def reset_phoneme_map():
    
    
    
    for key in inventories:
        
        generate_phonemes(dictionish, key)

    """
    global phoneme_map
    phoneme_map= {}
    for member in set_map["bakovichean_phonemes"]['All Phonemes']:
        phoneme_map[member.name] = member
    """


reset_phoneme_map()












#set map may have become obselete by forming a conjunction with phoneme map and inventories.
#print (set_map)
#


#################### Ok now we have mostly GUI related code ###########################3

# pickle_in = open("phoneme_data","rb")
# set_map = pickle.load(pickle_in)

#class_tuples = [('bakovicean_phoneme',['consonantal','syllabic','sonorant','approximant','voice','spreadG','constrG','continuant',
#                                                          'lateral','delR','nasal','labial','round','coronal','anterior','distributed','strident',
#                                                          'dorsal','high','low','front','back','atr'])]



"""
technical_map = {"bakovicean_phoneme":{ "keyCategories" : {'Vowels': (('syllabic', True),),
                       'Voiced Stops': (('continuant', False), ('delR', False), ('sonorant', False), ('voice', True)),
                       'Voiceless Stops': (
                       ('continuant', False), ('delR', False), ('sonorant', False), ('voice', False)),
                       'Voiced Affricates': (
                       ('continuant', False), ('delR', True), ('sonorant', False), ('voice', True)),
                       'Voiceless Affricates': (
                       ('continuant', False), ('delR', True), ('sonorant', False), ('voice', False)),
                       'Voiced Fricatives': (
                       ('continuant', True), ('delR', True), ('sonorant', False), ('voice', True)),
                       'Voiceless Fricatives': (
                       ('continuant', True), ('delR', True), ('sonorant', False), ('voice', False)),
                       'Nasals': (('nasal', True),),
                       'Sonorants': (('sonorant', True),)},"entailments":1},}
"""
class universal_signal(QObject):
    trigger =pyqtSignal()
    def set_off(self):
        self.trigger.emit()
added_new_sound = universal_signal()
inventory_update = universal_signal()

assistive_click_target = None


#for member in set_map["bakovicean_phoneme"]['All Phonemes']:
 #   phoneme_map[member.name]= member


#colors
light_gray = QColor(226,226,226)
light_red = QColor(255,209,183)
light_green = QColor(213,255,109)
light_teal = QColor(191,251,255)
light_yellow = QColor(253,255,135)
light_orange = QColor(255,195,84)
light_brown = QColor(198,109,57)
class the_main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.executive_window = executive_window()
        self.setCentralWidget(self.executive_window)

        # new_window
        new_window = QAction('&Import Datapack', self)
        new_window.setShortcut("Ctrl+I")
        new_window.setStatusTip('Import a Datapack')
        new_window.triggered.connect(partial(import_file_dialog,self.executive_window))

        # inspect_window

        inspect_window = QAction('&Inspect', self)
        inspect_window.setShortcut("Ctrl+I")
        inspect_window.setStatusTip('Inspect Inventories and Phonemes')
        inspect_window.triggered.connect(self.show_inspect)

        # build inventory
        build_inventory = QAction('&Inventory Builder',self)
        build_inventory.setShortcut("Ctrl+B")
        build_inventory.setStatusTip('Create new Inventories out of Existing Phonemes')
        build_inventory.triggered.connect(self.show_build_inventory)

        # build phoneme
        build_phoneme = QAction('&Phoneme Builder',self)
        build_phoneme.setShortcut("Ctrl+P")
        build_phoneme.setStatusTip('Create a New Phoneme')
        build_phoneme.triggered.connect(self.show_build_phoneme)

        # IPA symbol Palette
        IPA_palette = QAction('&IPA Symbol Palette',self)
        IPA_palette.setShortcut("Ctrl+L")
        IPA_palette.setStatusTip("Open a Palette whence you Can Copy and Paste Symbols")
        IPA_palette.triggered.connect(self.show_IPA_palette)


        # Featureset creator

        new_feature_set = QAction('&Create New Featureset',self)
        new_feature_set.setStatusTip('Create a new set of features with which to define phonemes')
        new_feature_set.setShortcut("Ctrl+F")
        new_feature_set.triggered.connect(self.show_build_featureset)

        # Featureset Editor
        new_featureset_editor = QAction('&Edit a Featureset',self)
        new_featureset_editor.setStatusTip('Edit an Already Extant Featureset')
        new_featureset_editor.setShortcut("Ctrl+E")
        new_featureset_editor.triggered.connect(self.show_edit_featureset)

        # Trashcan

        new_trashcan = QAction('&Trashcan',self)
        new_trashcan.setStatusTip("&Delete a Phoneme, Language or Feature-set")
        new_trashcan.triggered.connect(self.show_trashcan)

        # edit groups
        new_group_edit = QAction('&Edit a Phoneme Group',self)
        new_group_edit.setStatusTip('Edit several phonemes at once')
        new_group_edit.triggered.connect(self.show_group_edit)

        # Data_transfer

        new_data_transfer = QAction('&Transfer Data',self)
        new_data_transfer.setStatusTip('Transfer Data from one feature set to another')
        new_data_transfer.triggered.connect(self.show_data_transfer)

        # Datapack Management
        datapack_management = QAction('&Export Datapacks', self)
        datapack_management.setStatusTip('Create and Send Out Datapacks')
        datapack_management.triggered.connect(self.show_datapack_management)

        # Save
        Save_all = QAction('&Save',self)
        Save_all.setShortcut("Ctrl+S")
        Save_all.setStatusTip("Save your Data for Use in Later Sessions")
        Save_all.triggered.connect(self.save_data)
        self.save_needed = False

        self.statusBar()
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(IPA_palette)
        file_menu.addAction(inspect_window)
        file_menu.addAction(build_phoneme)
        file_menu.addAction(build_inventory)
        file_menu.addAction(new_feature_set)
        file_menu.addAction(new_trashcan)
        file_menu.addAction(new_featureset_editor)
        file_menu.addAction(new_group_edit)
        file_menu.addAction(new_data_transfer)
        file_menu.addAction(datapack_management)
        file_menu.addAction(new_window)
        file_menu.addAction(Save_all)
        self.setWindowTitle("Natural Class Finder")
        self.setWindowIcon(QtGui.QIcon('pictures/main logo.png'))
        self.show()

        added_new_sound.trigger.connect(self.save_needed_check)
        inventory_update.trigger.connect(self.save_needed_check)
    def save_needed_check(self):
        self.save_needed = True
    def save_data(self):
        pickle_out = open("feature_set_map","wb")
        pickle.dump(feature_set_map,pickle_out)
        pickle_out.close()
        pickle_out = open("dictionish","wb")
        pickle.dump(dictionish,pickle_out)
        pickle_out.close()
        pickle_out = open("inventories","wb")
        pickle.dump(inventories,pickle_out)
        pickle_out.close()
        pickle_out = open("technical_map","wb")
        pickle.dump(technical_map,pickle_out)
        pickle_out.close()
        hey_man = QtWidgets.QMessageBox.information(self,'Data Saved!','You Have Successfully Saved all of your Data.',QMessageBox.Ok)
        self.save_needed = False
    def make_new(self):
        self.newbie = executive_window()
        self.newbie.setGeometry(100, 100, 500, 200)
        self.newbie.show()

    def show_inspect(self):
        self.the_inspect_window = inspect_window()
        self.the_inspect_window.show()
    def show_build_inventory(self):
        self.inventory_builder = build_inventory_widget()
    def show_build_phoneme(self):
        self.phoneme_builder = build_phoneme_widget_stack()
    def show_IPA_palette(self):
        self.symbol_palette = symbol_palette()

    def closeEvent(self, QCloseEvent):
        hey_man = QtWidgets.QMessageBox.question(self,'Exiting Program','Are You Sure You Want to Quit the Application?',QMessageBox.Yes|QMessageBox.No)
        if hey_man == QMessageBox.Yes:
            if self.save_needed == True:
                hey_again_man = QtWidgets.QMessageBox.question(self, 'You Didn\'t Save!!!',
                                                         'Are You Really Sure that You Want to Exit Without saving?',
                                                         QMessageBox.Yes | QMessageBox.No)
                if hey_again_man == QMessageBox.Yes:
                    QCloseEvent.accept()
                else:
                    QCloseEvent.ignore()
            else:
                QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

    def show_build_featureset(self):
        self.feature_set_builder = build_featureset(self)
    def show_edit_featureset(self):
        self.feature_set_editor = edit_featureset_opening_page()

    def show_data_transfer(self):
        self.data_transfer = data_transfer()

    def show_datapack_management(self):
        self.datapack_management = data_pack_management()
    def show_group_edit(self):
        self.group_edit = alter_group_of_phonemes_opening_page()

    def show_trashcan(self):
        self.trashcan = trash_can(self)
class executive_window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        # initiating widgets
        self.exec_button = QtWidgets.QPushButton('Run Program')
        # self.selected_inventory = QtWidgets.QLabel('Select a Phoneme Inventory')
        self.inclusive_line = QtWidgets.QLineEdit()
        self.exclusive_line = QtWidgets.QLineEdit()
        self.inclusive_line_button = QtWidgets.QPushButton('Select Inclusive')
        self.exclusive_line_button = QtWidgets.QPushButton('Select Exclusive')
        self.inclusive_line_label = QtWidgets.QLabel("Choose your Phonemes to Include (split on comma)")
        self.exclusive_line_label = QtWidgets.QLabel("Choose your Phonemes to Exclude (split on comma)")
        self.inclusive_assistive_click = QtWidgets.QPushButton("Assistive Click")
        self.exclusive_assistive_click = QtWidgets.QPushButton("Assistive Click")
        ## Feature set selection
        #Just changed this from set_map to feature_set map... that may or may not goof stuff up. Should be good tho.
        self.inventories = [a for a in feature_set_map]
        self.chooseInventory = QComboBox()
        self.chooseInventory.setFixedWidth(100)
        self.chooseLanguage = QComboBox()
        self.chooseLanguage.setFixedWidth(100)
        self.chooseInventory.setDuplicatesEnabled(False)
        self.chooseInventory.addItem('Null')
        self.chooseLanguage.addItem("Null")
        self.update_inventory_list()

        # initiating variables

        # self.chosenInventory = []
        self.inclusive = []
        self.exclusive = []
        self.answer_windows =[]
        # choose inventories

        h_box0 = QtWidgets.QHBoxLayout()
        h_box0.addStretch()
        h_box0.addWidget(self.chooseInventory)
        h_box0.addWidget(self.chooseLanguage)
        h_box0.addStretch()

        h_box1 = QtWidgets.QHBoxLayout()
        h_box1.addStretch()
        # h_box1.addWidget(self.selected_inventory)
        #h_box1.addWidget(self.chooseInventory)
        h_box1.addStretch()

        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addStretch()
        h_box2.addWidget(self.inclusive_line)
        h_box2.addWidget(self.inclusive_line_button)
        h_box2.addWidget(self.inclusive_line_label)
        h_box2.addWidget(self.inclusive_assistive_click)
        h_box2.addStretch()

        h_box3 = QtWidgets.QHBoxLayout()
        h_box3.addStretch()
        h_box3.addWidget(self.exclusive_line)
        h_box3.addWidget(self.exclusive_line_button)
        h_box3.addWidget(self.exclusive_line_label)
        h_box3.addWidget(self.exclusive_assistive_click)
        h_box3.addStretch()
        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(h_box0)
        v_box.addLayout(h_box1)
        v_box.addLayout(h_box2)
        v_box.addLayout(h_box3)
        v_box.addWidget(self.exec_button)

        self.setLayout(v_box)
        self.setWindowTitle('Natural Class Finder')

        # clicking

        #self.chooseInventory.activated[str].connect(self.show_inventory)
        #inventory_update.trigger.connect(self.update_inventory_list)
        self.inclusive_line_button.clicked.connect(self.assign_phonemes)
        self.exclusive_line_button.clicked.connect(self.assign_phonemes)
        self.exec_button.clicked.connect(self.main_function)
        self.inclusive_assistive_click.clicked.connect(partial(self.pop_assistive_click_up,self.inclusive_line))
        self.exclusive_assistive_click.clicked.connect(partial(self.pop_assistive_click_up,self.exclusive_line))
        self.chooseInventory.activated[str].connect(self.update_language_list)
        self.assistive_click_window = None

        self.languages = 0

        self.show()

    def update_language_list(self):
        for number in range(self.languages):
            self.chooseLanguage.removeItem(1)
            self.languages -= 1
        for language in inventories[self.chooseInventory.currentText()]:
            self.chooseLanguage.addItem(language)
            self.languages += 1

    def pop_assistive_click_up(self,target):
        if self.chooseInventory.currentText() == "Null" or self.chooseLanguage.currentText()=="Null":
            hey_man = QtWidgets.QMessageBox.warning(self, "Pick an Inventory and a Language First!",
                                                    "You need to select a feature set inventory first", QMessageBox.Ok)
        else:
            self.assistive_click_window = assistive_click(self,target,self.chooseInventory.currentText(),self.chooseLanguage.currentText())

    def assign_phonemes(self):
        if self.chooseInventory.currentText() == "Null" or self.chooseLanguage.currentText() == "Null":
            hey_man = QtWidgets.QMessageBox.warning(self,"Pick an Inventory First!","You need to pick a feature set and a phoneme inventory before doing anything",
                                                    QMessageBox.Ok)
            return None
        the_input = self.inclusive_line.text()
        the_input = re.sub(' ','',the_input)
        exclusive_input = self.exclusive_line.text()
        exclusive_input = re.sub(' ', '', exclusive_input)
        def are_they_all_there(to_split):
            elements = re.split(',',to_split)
            checker = True
            for element in elements:
                if element in inventories[self.chooseInventory.currentText()][self.chooseLanguage.currentText()]:
                    pass
                elif element == '':
                    pass
                else:
                    checker = False
            return checker
        sender = self.sender()
        if sender.text() == 'Select Inclusive':
            if the_input == '':
                hey_man = QMessageBox.warning(self, "Pick Phonemes First!", "Hey, you Gotta Pick Some Phonemes First. Remember to Split on Commas",
                                               QMessageBox.Ok)
            elif are_they_all_there(the_input)== False:
                hey_man = QMessageBox.warning(self, "Phoneme Not Found", "One of Those Phonemes that You Entered Doesn't Exist",
                                               QMessageBox.Ok)
            else:
                self.inclusive_line_label.setText("You Have Selected: %s" % (the_input))
                self.inclusive = []
                for phoneme in re.split(',', the_input):
                    # I have to put this if statement here, kuz when you split it, it will return a nothing character at the end :(
                    if phoneme != '':
                        member = phoneme_map[self.chooseInventory.currentText()][phoneme]
                        self.inclusive.append(member)
        elif sender.text() == 'Select Exclusive':
            if exclusive_input == '':
                self.exclusive = []
                self.exclusive_line_label.setText("You Have Opted to not Exclude any Phonemes")
            elif are_they_all_there(exclusive_input) == False:
                hey_man = QMessageBox.question(self, "Phoneme Not Found","One of Those Phonemes that You Entered Doesn't Exist",QMessageBox.Ok)
            else:
                self.exclusive_line_label.setText("You Have Selected: %s" % (exclusive_input))
                self.exclusive = []
                for excludable in re.split(',', exclusive_input):
                    if excludable != '':
                        member = phoneme_map[self.chooseInventory.currentText()][excludable]
                        self.exclusive.append(member)
    def main_function(self):
        if len(self.inclusive) == 0:
            hey_man = QMessageBox.warning(self, "No Phonemes Selected!", "Hey, You Gotta Pick Stuff First!", QMessageBox.Ok)
        else:
            window = answer_display()
            self.answer_windows.append(window)
            window.show()
            find_natural_class(self.inclusive, self.exclusive,window,self.chooseInventory.currentText(),self.chooseLanguage.currentText())
    def update_inventory_list(self):
        for number in range(len(self.inventories)):
            self.chooseInventory.removeItem(1)

        for item in feature_set_map:
            self.chooseInventory.addItem(item)
            if item not in self.inventories:
                self.inventories.append(item)

class assistive_click(QtWidgets.QWidget):
    def __init__(self,parent = None,target = None,inventory = None, language = None, clear_out = False, painettava_nappi = None):
        super().__init__()
        self.parent = parent
        self.target = target
        self.painettava_nappi = painettava_nappi
        self.chosenInventory = inventory
        self.chosenLanguage  = language
        self.clear_out = clear_out
        self.init_ui()
    def init_ui(self):
        self.setWindowIcon(QtGui.QIcon('pictures/click.png'))
        self.grand_h_box = QtWidgets.QHBoxLayout()
        self.column_map = {}
        self.column_count_map = {}
        self.column_headers = [a for a in technical_map[self.chosenInventory]["keyCategories"]]
        self.column_headers.append("Other")
        for header in self.column_headers:
            new_col = QtWidgets.QVBoxLayout()
            self.grand_h_box.addLayout(new_col)
            self.column_map[header] = new_col
            new_col.addWidget(QtWidgets.QLabel(header))
            self.column_count_map[header] = 1

      #### the code under here has to do with filling it all out with the buttons and stuff
        asutettuja =[]
        asutettava = [a for a in inventories[self.chosenInventory][self.chosenLanguage]]

        for phoneme in inventories[self.chosenInventory][self.chosenLanguage]:

            ### getting access to the actual phoneme
            actual_phoneme = phoneme_map[self.chosenInventory][phoneme]
            ## checking each category, one at at time, to see if the phoneme works under it.
            for keyCategory in technical_map[self.chosenInventory]["keyCategories"]:
                parameters = []
                for parameter in technical_map[self.chosenInventory]["keyCategories"][keyCategory]:
                    parameters.append(parameter)

                add_me = True

                for parameter in parameters:
                    if getattr(actual_phoneme, parameter[0]) != parameter[1]:
                        add_me = False
                if add_me == True and phoneme not in asutettuja:
                    new_btn = QtWidgets.QPushButton(text=phoneme)
                    new_btn.clicked.connect(partial(insert_phoneme,new_btn,self.target,self.clear_out))
                    if self.painettava_nappi != None:
                        new_btn.clicked.connect(partial(click_other,self.painettava_nappi))
                    else:
                        pass
                    self.column_map[keyCategory].addWidget(new_btn)
                    self.column_count_map[keyCategory] += 1
                    ## add clickability here
                    asutettuja.append(phoneme)

        asutettava = [a for a in asutettava if a not in asutettuja]
        for phoneme in asutettava:
            new_btn = QtWidgets.QPushButton(text=phoneme)
            new_btn.clicked.connect(partial(insert_phoneme,new_btn,self.target,self.clear_out))
            if self.painettava_nappi != None:
                new_btn.clicked.connect(partial(click_other, self.painettava_nappi))
            else:
                pass
            self.column_map["Other"].addWidget(new_btn)
            self.column_count_map["Other"] += 1
            ## add clickability here
            asutettuja.append(phoneme)

        self.setLayout(self.grand_h_box)

        """
        global assistive_click_target
        if self.inclusive == True:
            assistive_click_target = self.parent.inclusive_line
        else:
            assistive_click_target = self.parent.exclusive_line
        """

        #### ok, now I need to fill in each column with some empty labels so that the columns look nice and even.
        highest_count = 0
        for key in self.column_count_map:
            if self.column_count_map[key] > highest_count:
                highest_count = self.column_count_map[key]

        for header in self.column_map:
            self.column_map[header].addStretch(highest_count-self.column_count_map[header])

        self.setWindowTitle("Assistive Click")
        self.show()
def insert_phoneme(button,target,clear_out):
    text = button.text()
    text += ','
    
    
    
    if isinstance(target,QtWidgets.QLineEdit):
        if clear_out:
            target.setText("")
        if clear_out == False:
            pass
        target.insert(text)
    elif isinstance(target,QtWidgets.QTextEdit):
        if clear_out:
            target.setText("")
        target.insertPlainText(text)
    #global assistive_click_target
    #assistive_click_target.insert(text)
def test_function():
    pass
def click_other(button):
    button.click()
class inspect_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # # you shouldn't ever need a bigger table, but hypothetically if you had
        # # a language with mroe than 25 phonemes in one of the given categories down there,
        # # they wouldn't show up when you hit inspect : /

        self.setWindowTitle('Inspection')
        self.setWindowIcon(QtGui.QIcon('pictures/inspect.png'))

        self.inventory_report = QTableWidget(30,10)
        self.phoneme_report = inspect_phoneme_widget()
        self.right_dock = QtWidgets.QDockWidget("Phoneme Report")
        self.picker= inspect_widget(self.inventory_report,self.phoneme_report,self)
        self.top_dock = QtWidgets.QDockWidget("Select Phonemes and Inventories")
        self.top_dock.setWidget(self.picker)
        self.right_dock.setWidget(self.phoneme_report)
        self.no_bar = QtWidgets.QWidget()
        self.also_no_bar = QtWidgets.QWidget()
        self.top_dock.setTitleBarWidget(self.no_bar)
        self.right_dock.setTitleBarWidget(self.also_no_bar)
        self.right_dock.toggleViewAction()
        self.setCentralWidget(self.inventory_report)
        self.addDockWidget(Qt.TopDockWidgetArea,self.top_dock)
        self.addDockWidget(Qt.RightDockWidgetArea,self.right_dock)
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("Inspection Panel")
        self.setGeometry(100,100,1490,400)
        self.show()
        self.test = "test"
        
        
        
        

class inspect_widget(QtWidgets.QWidget):
    def __init__(self, table,phoneme_inspection, parent=None):
        super(inspect_widget, self).__init__()
        self.table = table
        self.phoneme_inspection = phoneme_inspection
        self.parent = parent
        self.init_ui()

    def init_ui(self):

        # self.chooseInventory = QComboBox()
        self.inventories = ["Null",]
        self.chosenLanguage = [] ### ???
        self.languages = []

        self.chooseInventory = QComboBox()
        self.chooseInventory.setDuplicatesEnabled(False)
        self.chooseInventory.addItem('Null')
        self.chooseInventory.setFixedWidth(175)
        self.update_inventory_list()


        self.chooseLanguage = QComboBox()
        self.chooseLanguage.setDuplicatesEnabled(False)
        self.chooseLanguage.addItem('Null')
        self.chooseLanguage.setFixedWidth(150)
        self.chooseLanguage_label = QtWidgets.QLabel("Choose a Language")
        self.assistive_click = QtWidgets.QPushButton(text="Assistive Click")

        self.chooseInventory_label = QtWidgets.QLabel("Choose a Sound Inventory")
        self.phoneme_inspect_line = QtWidgets.QLineEdit()
        self.phoneme_inspect_line.setFixedWidth(35)
        self.phoneme_inspect_button = QtWidgets.QPushButton('Inspect Phoneme')
        self.phoneme_inspect_label = QtWidgets.QLabel("Choose a Single Phoneme to Inspect")

        h_box1 = QtWidgets.QHBoxLayout()
        h_box1.addStretch()
        h_box1.addWidget(self.chooseInventory)
        h_box1.addWidget(self.chooseInventory_label)
        h_box1.addWidget(self.chooseLanguage)
        h_box1.addWidget(self.chooseLanguage_label)
        h_box1.addWidget(self.assistive_click)
        h_box1.addStretch()

        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addStretch()
        h_box2.addWidget(self.phoneme_inspect_line)
        h_box2.addWidget(self.phoneme_inspect_button)
        h_box2.addWidget(self.phoneme_inspect_label)
        h_box2.addStretch()

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(h_box1)
        v_box.addLayout(h_box2)

        self.setLayout(v_box)

        # clicking
        self.phoneme_inspect_button.clicked.connect(self.report_phoneme)
        self.chooseInventory.activated[str].connect(self.update_language_list)
        self.chooseInventory.activated[str].connect(self.table.clearContents)
        # the next function may not be necessary any dalshe
        self.chooseInventory.activated[str].connect(self.update_for_phoneme_inspector)
        self.chooseInventory.activated[str].connect(self.renew_phoneme_inspector)
        self.chooseLanguage.activated[str].connect(self.populate_inventory)
        self.assistive_click.clicked.connect(partial(self.pop_assistive_click_up,self.phoneme_inspect_line))
        self.phoneme_inspect_line.textChanged[str].connect(partial(self.remove_comma,self.phoneme_inspect_line))
        inventory_update.trigger.connect(self.update_inventory_list)

        
        
        
        self.test = "murper"
        self.renew_phoneme_inspector()
        #

    def remove_comma(self,target):
        target.setText(re.sub(",","",target.text()))
    def pop_assistive_click_up(self,target):
        if self.chooseInventory.currentText() == "Null" or self.chooseLanguage.currentText()=="Null":
            hey_man = QtWidgets.QMessageBox.warning(self, "Pick an Inventory and a Language First!",
                                                    "You need to select a feature set inventory first", QMessageBox.Ok)
        else:
            inventory = self.chooseInventory.currentText()
            language = self.chooseLanguage.currentText()
            self.assistive_click_window = assistive_click(self,target,inventory,language,True,self.phoneme_inspect_button)

    def renew_phoneme_inspector(self):


        self.phoneme_inspection.close()
        new_phoneme_inspection = inspect_phoneme_widget()
        self.parent.phoneme_report = new_phoneme_inspection
        self.phoneme_inspection = new_phoneme_inspection
        
        
        
        
        self.parent.right_dock.setWidget(new_phoneme_inspection)
        #
        self.update_for_phoneme_inspector()
        self.phoneme_inspection.init_ui()

    def update_for_phoneme_inspector(self):

        self.phoneme_inspection.chosen_inventory = self.chooseInventory.currentText()

    def report_phoneme(self):
        
        
        if self.chooseInventory.currentText() == "Null":
            hey_man = QtWidgets.QMessageBox.warning(self,"Pick an Inventory First!","You need to select a feature set inventory first",QMessageBox.Ok)
            return None
        # !!! I might have goofed things up here, making a biggish change
        #attributes = [a for a in set_map[self.chooseInventory.currentText()]["All Phonemes"][0].attributes]
        attributes = [a for a in feature_set_map[self.chooseInventory.currentText()]]
        attributes = [a for a in attributes if a != "name"]
        the_input = self.phoneme_inspect_line.text()
        the_input = re.sub(' ','',the_input)
        

        if the_input == '':
            hey_man = QMessageBox.warning(self, "No Phoneme Selected", "You Need to Pick a Phoneme First", QMessageBox.Ok)
        elif ',' in the_input:
            hey_man = QMessageBox.warning(self, "More than One Phoneme Selected", "You Can Only Inspect One Phoneme at a Time", QMessageBox.Ok)
            # reminder! don't let anyone save a phoneme with a comma in it's name haha
        elif the_input not in inventories[self.chooseInventory.currentText()]["All Phonemes"]:
            
            hey_man = QMessageBox.warning(self, "Phoneme Not Found", "This Phoneme Doesn't Exist in the inventory called %s!"%(self.chooseInventory.currentText()), QMessageBox.Ok)
        else:
            chosen_phoneme = phoneme_map[self.chooseInventory.currentText()][the_input]
            
            self.phoneme_inspection.actual_subject.setText(chosen_phoneme.name)
            for attribute in attributes:
                value = getattr(chosen_phoneme,attribute)
                if value == True:
                    self.phoneme_inspection.value_map[attribute].setText('True')
                    self.phoneme_inspection.color_map[attribute].setPixmap(QtGui.QPixmap("pictures/green.png"))
                elif value == False:
                    self.phoneme_inspection.value_map[attribute].setText('False')
                    self.phoneme_inspection.color_map[attribute].setPixmap(QtGui.QPixmap("pictures/red.png"))

    def get_col_no(self, name):
        for number in range(self.table.columnCount()):
            header = self.table.horizontalHeaderItem(number).text()
            if header == name:
                return number
                break

    def populate_inventory(self, Text):
        
        chosen_inventory = self.chooseInventory.currentText()
        self.table.clearContents()

        # asutettava is Finnish for "to be populated"
        # I made an edit here on asutettava!
        if Text == 'Null':
            pass
        else:
            
            
            
            
            column_headers = [a for a in technical_map[self.chooseInventory.currentText()]["keyCategories"]]

            column_headers.append("Other")
            
            self.table.setColumnCount(len(column_headers))
            asutettava = [a for a in set_map[chosen_inventory][Text]]
            self.chosenLanguage= set_map[chosen_inventory][Text]

            asutettuja = []
            self.table.setHorizontalHeaderLabels(column_headers)
            item = QTableWidgetItem('10')
            
            for category in column_headers:
                if category in technical_map[self.chooseInventory.currentText()]["keyCategories"]:
                    col_no = self.get_col_no(category)
                    row_no = 0
                    for phoneme in asutettava:
                        add_me = True
                        for feature_value in technical_map[self.chooseInventory.currentText()]["keyCategories"][category]:
                            if getattr(phoneme, feature_value[0]) != feature_value[1]:
                                add_me = False
                            elif phoneme in asutettuja:
                                add_me = False
                        if add_me == True:
                            row_no += 1
                            asutettuja.append(phoneme)
                            item = QTableWidgetItem(phoneme.name)
                            self.table.setItem(row_no, col_no, item)

            # now to populate the others column :)
            asutettava = [a for a in asutettava if a not in asutettuja]
            row_no = 0
            col_no = self.get_col_no('Other')
            
            for phoneme in asutettava:
                row_no += 1
                item = QTableWidgetItem(phoneme.name)
                self.table.setItem(row_no, col_no, item)
                # item.setFlags(QTableWidgetItem.setFlags(
                #     Qt.ItemIsEditable | Qt.ItemIsEnabled))  ############3 This line isnt working :(
        
    def update_inventory_list(self):
        for number in range(len(self.inventories)):
            self.chooseInventory.removeItem(1)

        for item in feature_set_map:
            self.chooseInventory.addItem(item)
            if item not in self.inventories:
                self.inventories.append(item)

    def update_language_list(self):
        for number in range(len(self.languages)):
            self.chooseLanguage.removeItem(1)
        if self.chooseInventory.currentText() == "Null" or self.chooseInventory.currentText() == None:
            #hey_man = QtWidgets.QMessageBox.warning(self,"Pick an Inventory First!","You need to pick a feature set inventory first",QMessageBox.Ok)
            
            return None
        else:
            
            sound_set = self.chooseInventory.currentText()
            for item in inventories[sound_set]:
                self.chooseLanguage.addItem(item)
                if item not in self.languages:
                    self.languages.append(item)
            
    def show_inventory(self, Text):
        self.selected_inventory.setText("You Have Selected %s" % Text)
        if Text in inventories[self.chooseInventory.currentText()]:
            self.chosenLanguage = inventories[self.chooseInventory.currentText()][Text]
        elif Text == "Null":
            self.chosenLanguage = []
class inspect_phoneme_widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.chosen_inventory = "Null"
    def init_ui(self):
        
        if self.chosen_inventory == "Null":
            self.hide()
            pass
        else:

            self.actual_subject = QtWidgets.QLabel()
            h_box0 = QtWidgets.QHBoxLayout()
            h_box0.addStretch()
            h_box0.addWidget(self.actual_subject)
            h_box0.addStretch()
            self.subject = QtWidgets.QLabel("Chosen Phoneme")
            lh_box0 = QtWidgets.QHBoxLayout()
            lh_box0.addStretch()
            lh_box0.addWidget(self.subject)
            lh_box0.addStretch()
            ### this line needs to get replaced; it's a dangerous one.
            #self.attributes = [a for a in set_map[self.chosen_inventory]["All Phonemes"][0].attributes]
            self.attributes = [a for a in feature_set_map[self.chosen_inventory]]
            self.attributes = [a for a in self.attributes if a != "name"]

            rv_box = QtWidgets.QVBoxLayout()
            lv_box = QtWidgets.QVBoxLayout()
            rv_box.addLayout(h_box0)
            lv_box.addLayout(lh_box0)

            self.value_map = {}
            self.color_map = {}

            for att in self.attributes:
                self.__setattr__(att+"V",QtWidgets.QLabel("Null"))
                self.__setattr__(att+"P",QtWidgets.QLabel())
                self.__setattr__(att,QtWidgets.QLabel(att+ " :"))
                picture = self.__getattribute__(att+"P")
                picture.setPixmap(QtGui.QPixmap("pictures/grey.png"))

                self.value_map[att]=self.__getattribute__(att+"V")
                self.color_map[att]=self.__getattribute__(att+"P")

                rh_box = QtWidgets.QHBoxLayout()
                rh_box.addStretch()
                rh_box.addWidget(self.__getattribute__(att +"V"))
                rh_box.addWidget(self.__getattribute__(att +"P"))
                rh_box.addStretch()
                rv_box.addLayout(rh_box)

                lh_box = QtWidgets.QHBoxLayout()
                lh_box.addStretch()
                lh_box.addWidget(self.__getattribute__(att))
                lh_box.addStretch()
                lv_box.addLayout(lh_box)
            grand_hbox = QtWidgets.QHBoxLayout()
            grand_hbox.addLayout(lv_box)
            grand_hbox.addLayout(rv_box)
            self.setLayout(grand_hbox)
            self.show()
            #
            # self.consonantalV = QtWidgets.QLabel("Null")
            # self.consonantalP = QtWidgets.QLabel()
            # self.consonantalP.setPixmap(QtGui.QPixmap("pictures/grey.png"))
            #
            # h_box1 = QtWidgets.QHBoxLayout()
            # h_box1.addStretch()
            # h_box1.addWidget(self.consonantalV)
            # h_box1.addWidget(self.consonantalP)
            # h_box1.addStretch()



        ######## Left Hand Column
            #
            # ## Started counting from 2, haha my bad

            #
            #
            # self.consonantal = QtWidgets.QLabel("consonantal :")
            #
            # lh_box2 = QtWidgets.QHBoxLayout()
            # lh_box2.addStretch()
            # lh_box2.addWidget(self.consonantal)
            # lh_box2.addStretch()




            # self.value_map={'consonantal':self.consonantalV,'syllabic':self.syllabicV,'sonorant':self.sonorantV,'approximant':self.approximantV,
            #                'voice':self.voiceV,'spreadG':self.spreadGV,'constrG':self.constrGV,'continuant':self.continuantV,'lateral':self.lateralV,
            #                'delR':self.delRV,'nasal':self.nasalV,'labial':self.labialV,'round':self.roundV,'coronal':self.coronalV,'anterior':self.anteriorV,
            #                'distributed':self.distributedV,'strident':self.stridentV,'dorsal':self.dorsalV,'high':self.highV,'low':self.lowV,
            #                'front':self.frontV,'back':self.backV,'atr':self.atrV}
            # self.color_map={'consonantal':self.consonantalP,'syllabic':self.syllabicP,'sonorant':self.sonorantP,'approximant':self.approximantP,
            #                'voice':self.voiceP,'spreadG':self.spreadGP,'constrG':self.constrGP,'continuant':self.continuantP,'lateral':self.lateralP,
            #                'delR':self.delRP,'nasal':self.nasalP,'labial':self.labialP,'round':self.roundP,'coronal':self.coronalP,'anterior':self.anteriorP,
            #                'distributed':self.distributedP,'strident':self.stridentP,'dorsal':self.dorsalP,'high':self.highP,'low':self.lowP,
            #                'front':self.frontP,'back':self.backP,'atr':self.atrP}



class build_inventory_widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):

        self.setWindowIcon(QtGui.QIcon('pictures/inventory.png'))

        background = QtGui.QImage("pictures/inventory2.png")
        palette = QtGui.QPalette()
        palette.setBrush(10, QtGui.QBrush(background))
        self.setPalette(palette)

        self.top_frame = QtWidgets.QFrame()
        self.top_frame.setStyleSheet("background-color: %s;"%light_gray.name())

        self.top_frame_vbox = QtWidgets.QVBoxLayout(self.top_frame)
        self.top_frame_hbox = QtWidgets.QHBoxLayout()
        self.top_frame_hbox.addStretch(1)
        self.top_frame_hbox.addWidget(self.top_frame)
        self.top_frame_hbox.addStretch(1)

        self.combo_box_label = QtWidgets.QLabel("Select an inventory")
        self.combo_box_label.setStyleSheet("background-color: %s;" % light_gray.name())
        self.inventories = []

        self.chooseInventory = QComboBox()
        self.chooseInventory.setDuplicatesEnabled(False)
        self.chooseInventory.addItem('Null')
        self.update_inventory_list()

        self.chooseLanguage = QComboBox()
        self.chooseLanguage.setFixedWidth(100)
        self.chooseLanguage.addItem("Null")
        self.chooseLanguage_label = QtWidgets.QLabel("Choose a Language:")
        self.chooseLanguage_label.setStyleSheet("background-color: %s;" % light_gray.name())

        self.import_inventory_btn = QtWidgets.QPushButton("Import")
        self.instruction_label = QtWidgets.QLabel("Remember! Split on Commas! E.G. 'a,b,c' ")
        self.instruction_label.setStyleSheet("background-color: %s;"%light_gray.name())
        self.text_box = QTextEdit()
        self.save_as_label = QtWidgets.QLabel("Choose a Name:")
        self.save_as_label.setStyleSheet("background-color: %s;" % light_gray.name())
        self.save_as= QtWidgets.QLineEdit()
        self.save_btn = QtWidgets.QPushButton("Add")
        self.assumption_toggle = QtWidgets.QCheckBox()
        self.chosen_inventory = 'Null'

        h_box0 = QtWidgets.QHBoxLayout()
        h_box0.addStretch()
        h_box0.addWidget(self.combo_box_label)
        h_box0.addWidget(self.chooseInventory)
        h_box0.addStretch()
        h_box1 = QtWidgets.QHBoxLayout()
        h_box1.addStretch()
        h_box1.addWidget(self.chooseLanguage_label)
        h_box1.addWidget(self.chooseLanguage)
        h_box1.addWidget(self.import_inventory_btn)
        h_box1.addStretch()
        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addStretch()
        h_box2.addWidget(self.instruction_label)

        h_box2.addStretch()
        h_box3 = QtWidgets.QHBoxLayout()
        h_box3.addStretch()
        h_box3.addWidget(self.text_box)
        h_box3.addStretch()

        self.bottom_frame = QtWidgets.QFrame()
        self.bottom_frame.setStyleSheet("background-color: %s;"%light_gray.name())
        self.bottom_frame_hbox = QtWidgets.QHBoxLayout()
        self.bottom_frame_hbox.addStretch(1)
        self.bottom_frame_hbox.addWidget(self.bottom_frame)
        self.bottom_frame_hbox.addStretch(1)
        h_box4 = QtWidgets.QHBoxLayout(self.bottom_frame)
        h_box4.addStretch()
        h_box4.addWidget(self.save_as_label)
        h_box4.addWidget(self.save_as)
        h_box4.addWidget(self.save_btn)
        h_box4.addStretch()


        v_box = QtWidgets.QVBoxLayout()
        self.top_frame_vbox.addLayout(h_box0)
        self.top_frame_vbox.addLayout(h_box1)
        self.top_frame_vbox.addLayout(h_box2)
        v_box.addLayout(self.top_frame_hbox)
        v_box.addLayout(h_box3)
        v_box.addLayout(self.bottom_frame_hbox)



        self.setLayout(v_box)
        self.setGeometry(643,279,473,373)

        self.setWindowTitle('Inventory Builder')
        self.show()

        #clicking
        self.import_inventory_btn.clicked.connect(self.import_phonemes)
        self.chooseInventory.activated[str].connect(self.select_inventory)
        self.chooseInventory.activated[str].connect(self.update_language_list)
        self.save_btn.clicked.connect(self.save_inventory)
        inventory_update.trigger.connect(self.update_inventory_list)

        # so that you can remove stuff from the combo box
        self.language_count = 0
        self.chosen_language = "Null"
    def update_language_list(self):
        for number in range(self.language_count):
            self.language_count -= 1
            self.chooseLanguage.removeItem(1)
        if self.chooseInventory.currentText() == "Null":
            pass
        else:
            for key in inventories[self.chooseInventory.currentText()]:
                self.chooseLanguage.addItem(key)
                self.language_count += 1
    def select_inventory(self,Text):
        self.chosen_inventory = Text

    def import_phonemes(self):

        self.chosen_inventory = self.chooseInventory.currentText()
        self.chosen_language = self.chooseLanguage.currentText()

        
        
        print (self.chosen_language in inventories[self.chosen_inventory])
        if self.chosen_language == 'Null' or self.chosen_inventory == 'Null':
            hey_man = QMessageBox.warning(self,"Choose an Inventory!","You Gotta Pick a language First", QMessageBox.Ok)
        elif self.chosen_language in inventories[self.chosen_inventory]:
            language = inventories[self.chosen_inventory][self.chosen_language]
            language_string = ''
            for member in language:
                language_string +=member
                language_string +=','
                language_string +=' '
            self.text_box.setText(language_string)

    def save_inventory(self):
        inventory_name = self.save_as.text()
        new_inventory = []
        the_input = self.text_box.toPlainText()
        the_input = re.sub(' ', '', the_input)
        if inventory_name == '' or the_input == '':
            hey_man = QtWidgets.QMessageBox.warning(self,"Input Missing!!!","You Need to Put in Phonemes and Choose a Name for the New Inventory.",QMessageBox.Ok)
            return False
        elif self.are_they_all_there(the_input) == False:
            hey_man = QtWidgets.QMessageBox.warning(self, "Unacceptable Phoneme",
                                                    "One of the phonemes in the provided list does not exist.")
            return False
        name_list = the_input.split(',')

        check_input_again = re.sub(' ','',the_input)
        check_input_again = re.sub(',','',the_input)
        if check_input_again  == '':
            hey_man = QtWidgets.QMessageBox.warning(self, "Input Missing!!!",
                                                    "You Need to Put in Phonemes and Choose a Name for the New Inventory.",
                                                    QMessageBox.Ok)
            return False
        else:
            pass

        # for whatever reason, the function threw a hissy fit because
        # there was an extra nothing character at the end, so that's why I need this next line here.
        name_list = [a for a in name_list if a != '']
        
        # you don't need to directly change the set_map anymore, so i've greyed this next line out.
        #phoneme_list= [phoneme_map[a] for a in name_list]
        
        if inventory_name == "All Phonemes":
            hey_man = QtWidgets.QMessageBox.warning(self,"Unacceptable Name","Hey look, You Just Can't Name It that or You'll Ruin the System!",QMessageBox.Ok)
        elif inventory_name in inventories[self.chosen_inventory]:
            hey_man = QtWidgets.QMessageBox.warning(self,"Overwrite Inventory?","You Will Overwrite an extant Inventory. Are You Sure?",QMessageBox.Yes | QMessageBox.No)
            if hey_man == QtWidgets.QMessageBox.Yes:
                # I don't think you need to directly change the set_map anymore, So I've greyed it out
                #set_map[inventory_name] = phoneme_list
                inventories[self.chosen_inventory][inventory_name]= name_list
                hey_man = QtWidgets.QMessageBox.information(self, "New Inventory Added",
                                                        "Added a New Inventory Named %s" % (inventory_name),QMessageBox.Ok)
            elif hey_man == QtWidgets.QMessageBox.No:
                pass
        else:
            # same thing here, dude
            #set_map[inventory_name] = phoneme_list
            inventories[self.chosen_inventory][inventory_name] = name_list
            hey_man = QtWidgets.QMessageBox.information(self,"New Inventory Added", "Added a New Inventory Named %s"% (inventory_name),QMessageBox.Ok)
        inventory_update.set_off()
        # I think we can effectively reset the set_map by just doing this:
        reset_phoneme_map()

    def are_they_all_there(self,to_split):
        elements = re.split(',', to_split)
        checker = True
        for element in elements:
            if element in inventories[self.chosen_inventory]["All Phonemes"]:
                pass
            elif element == '':
                pass
            else:
                checker = False
        return checker
    def update_inventory_list(self):
        for number in range(len(self.inventories)):
            self.chooseInventory.removeItem(1)

        for item in feature_set_map:
            self.chooseInventory.addItem(item)
            if item not in self.inventories:
                self.inventories.append(item)

class build_phoneme_widget_stack(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.page1 = build_phoneme_opening_page(self)
        self.page2 = build_phoneme_widget(self)
        self.addWidget(self.page1)
        self.addWidget(self.page2)
        self.setCurrentWidget(self.page1)
        self.setWindowTitle("Phoneme Builder")
        self.setWindowIcon(QtGui.QIcon('pictures/building.png'))
        self.show()
class build_phoneme_opening_page(QtWidgets.QWidget):
    def __init__(self,parent = None):
        super().__init__()
        self.parent = parent
        self.init_ui()
    def init_ui(self):
        #self.setStyleSheet("background-color: %s;"%light_red.name())

        self.layout = QtWidgets.QVBoxLayout()

        self.logo = QtGui.QPixmap('pictures/building.png')
        self.logo = self.logo.scaled(250, 150, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.picture = QtWidgets.QLabel()
        self.picture.setPixmap(self.logo)
        self.picture.setFixedWidth(250)
        self.layout.addWidget(self.picture)


        self.prompt = QtWidgets.QLabel("Choose Which Feature Set To Make A Phoneme With")

        self.layout.addWidget(self.prompt)
        self.choose_box = QtWidgets.QComboBox()

        self.choose_box.addItem("Null")
        for key in feature_set_map:
            self.choose_box.addItem(key)
        self.layout.addWidget(self.choose_box)
        self.next_btn = QtWidgets.QPushButton("Next")

        self.next_btn.clicked.connect(self.next_page)
        self.layout.addWidget(self.next_btn)
        self.setLayout(self.layout)
        self.show()


    def next_page(self):
        if self.choose_box.currentText() == "Null":
            hey_man = QtWidgets.QMessageBox.warning(self, "Pick a Featureset First!", "You need to pick the Feature Set the New Phoneme Will Belong to First.",
                                                        QMessageBox.Ok)
        else:
            self.parent.setCurrentWidget(self.parent.page2)
            self.parent.page2.fill_it_all_out()
            self.parent.page2.chosenInventory = self.choose_box.currentText()
            self.parent.page2.update_language_list()
class build_phoneme_widget(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):

        #Qframe
        self.left_frame = QtWidgets.QFrame()

        self.left_frame.setStyleSheet("background-color: %s;"%light_red.name())


        self.advice_label = QtWidgets.QLabel("Base off of Another Phoneme")
        self.import_line = QtWidgets.QLineEdit()
        self.import_line.setStyleSheet("background-color: white;")
        self.assistive_click_btn = QtWidgets.QPushButton("Assistive Click")
        self.assistive_click_btn.setStyleSheet("background-color: %s;"%light_gray.name())
        self.import_btn = QtWidgets.QPushButton("Load")
        self.import_btn.setStyleSheet("background-color: %s;"%light_gray.name())
        self.feature_assumption_toggle = QtWidgets.QCheckBox("Toggle Assume Features")

        self.inventories = [a for a in feature_set_map]
        self.chosenInventory = self.parent.page1.choose_box.currentText()
        self.attributes = []

        self.chooseInventory = QComboBox()
        self.chooseInventory.setDuplicatesEnabled(False)
        self.chooseInventory.setStyleSheet("background-color: white;")
        #self.chooseInventory.addItem('Null') ### you don't really need Null, when you think about it, if "All phonemes" is there.
        self.chooseInventoryLabel = QtWidgets.QLabel("Choose a Target Inventory to Save into")


        #self.chooseFeatureSet = QComboBox()
        #self.chooseFeatureSetLabel = QtWidgets.QLabel("Choose a feature set inventory!")
        #self.update_inventory_list()
        self.save_btn = QtWidgets.QPushButton("Add")
        self.save_btn.setStyleSheet("background-color: %s;"%light_gray.name())
        self.save_as_line_advice = QtWidgets.QLabel("Choose the Phoneme's new Symbol")
        self.save_as_line = QtWidgets.QLineEdit()
        self.save_as_line.setStyleSheet("background-color: white;")
        self.optionsVBox= QtWidgets.QVBoxLayout(self.left_frame)

        """
        self.oHBox1 = QtWidgets.QHBoxLayout()
        self.oHBox1.addStretch()
        self.oHBox1.addWidget(self.chooseFeatureSetLabel)
        self.oHBox1.addStretch()

        self.oHBox2 = QtWidgets.QHBoxLayout()
        self.oHBox2.addStretch()
        self.oHBox2.addWidget(self.chooseFeatureSet)
        self.oHBox2.addStretch() """

        self.oHBox3 = QtWidgets.QHBoxLayout()
        self.oHBox3.addStretch(1)
        self.oHBox3.addWidget(self.advice_label) ### your gonna need to get this to work tho
        self.oHBox3.addStretch(1)

        self.oHBox4 = QtWidgets.QHBoxLayout()
        self.oHBox4.addStretch()
        self.oHBox4.addWidget(self.import_line)
        self.oHBox4.addStretch()

        self.ohBox4point5 = QtWidgets.QHBoxLayout()
        self.ohBox4point5.addStretch()
        self.ohBox4point5.addWidget(self.assistive_click_btn)
        self.ohBox4point5.addStretch()

        self.oHBox6 = QtWidgets.QHBoxLayout()
        self.oHBox6.addStretch()
        self.oHBox6.addWidget(self.import_btn)
        self.oHBox6.addStretch()

        self.oHBox5 = QtWidgets.QHBoxLayout()
        self.oHBox5.addStretch()
        self.oHBox5.addWidget(self.feature_assumption_toggle)
        self.oHBox5.addStretch()

        self.oHBox7 = QtWidgets.QHBoxLayout()
        self.oHBox7.addStretch()
        self.oHBox7.addWidget(self.chooseInventoryLabel)
        self.oHBox7.addStretch()

        self.oHBox8 = QtWidgets.QHBoxLayout()
        self.oHBox8.addStretch()
        self.oHBox8.addWidget(self.chooseInventory)
        self.oHBox8.addStretch()

        self.oHBox9 = QtWidgets.QHBoxLayout()
        self.oHBox9.addStretch()
        self.oHBox9.addWidget(self.save_as_line_advice)
        self.oHBox9.addStretch()

        self.oHBox10 = QtWidgets.QHBoxLayout()
        self.oHBox10.addStretch()
        self.oHBox10.addWidget(self.save_as_line)
        self.oHBox10.addStretch()

        self.oHBox11 = QtWidgets.QHBoxLayout()
        self.oHBox11.addStretch()
        self.oHBox11.addWidget(self.save_btn)
        self.oHBox11.addStretch()

        #self.optionsVBox.addLayout(self.oHBox1)
        #self.optionsVBox.addLayout(self.oHBox2)
        self.optionsVBox.addLayout(self.oHBox3)
        self.optionsVBox.addLayout(self.oHBox4)
        self.optionsVBox.addLayout(self.ohBox4point5)
        self.optionsVBox.addLayout(self.oHBox5)
        self.optionsVBox.addLayout(self.oHBox6)
        self.optionsVBox.addLayout(self.oHBox7)
        self.optionsVBox.addLayout(self.oHBox8)
        self.optionsVBox.addLayout(self.oHBox9)
        self.optionsVBox.addLayout(self.oHBox10)
        self.optionsVBox.addLayout(self.oHBox11)
        self.grand_hbox = QtWidgets.QHBoxLayout()
        #self.grand_hbox.addLayout(self.optionsVBox)
        self.grand_hbox.addWidget(self.left_frame)

        self.setLayout(self.grand_hbox)
        self.setWindowTitle("Phoneme Builder")
        self.show()

        #clicking

        self.import_btn.clicked.connect(self.populate_phoneme)
        #self.chooseFeatureSet.activated[str].connect(self.fill_it_all_out)
        self.feature_assumption_toggle.stateChanged.connect(self.recursive_assume)
        self.save_btn.clicked.connect(self.save_phoneme) ### and this
        #inventory_update.trigger.connect(self.update_inventory_list)
        added_new_sound.trigger.connect(reset_phoneme_map) ### prollly wanna change this tbh
        self.assistive_click_btn.clicked.connect(self.show_assistive_click)
        self.import_line.textChanged[str].connect(
            partial(self.remove_comma, self.import_line))


    def fill_it_all_out(self):
        # code for resetting the thing here
        # for luku in range (1,self.grand_hbox.count()):
        #     self.grand_hbox.removeItem(self.grand_hbox.itemAt(luku))
        #     
        #

        # I think I was right in changing the right side from self.chooseFeatureset.currentText() to nothing
        # and then having the next page button define it.
        #self.chosenInventory = self.chooseFeatureSet.currentText()

        ## ok this line needed to be changed. I want to get the attributes from the class tuples thing instead, that's neater
        #self.attributes = [a for a in set_map[self.chosenInventory]["All Phonemes"][0].attributes]
        for key in feature_set_map:
            
            if key == self.parent.page1.choose_box.currentText():
                
                self.attributes = feature_set_map[key]

        number_of_columns = 2*(math.ceil(len(self.attributes)/10))

        column_map = {}
        self.value_map = {}
        self.color_map = {}
        for number in range(number_of_columns):
            new_col = QtWidgets.QVBoxLayout()
            column_map[("column"+str(number))]= new_col

        # tal is swedish for number
        for tal in range(len(self.attributes)):
            col_no = 2*(math.floor(tal/10))

            new_label = QtWidgets.QLabel(self.attributes[tal]+":")
            new_button= QtWidgets.QPushButton("Null")
            new_pic  = QtWidgets.QLabel()
            new_pic.setPixmap(QtGui.QPixmap("pictures/grey.png"))
            new_button.clicked.connect(self.alter_value)
            new_button.clicked.connect(partial(self.recursive_assume,new_button))

            self.value_map[self.attributes[tal]] = new_button
            self.color_map[self.attributes[tal]] = new_pic

            new_lhbox = QtWidgets.QHBoxLayout()
            new_lhbox.addStretch()
            new_lhbox.addWidget(new_label)
            new_lhbox.addStretch()

            new_hbox = QtWidgets.QHBoxLayout()
            new_hbox.addStretch()
            new_hbox.addWidget(new_button)
            new_hbox.addWidget(new_pic)
            new_hbox.addStretch()

            column_map[("column"+str(col_no))].addLayout(new_lhbox)
            column_map[("column" + str(col_no+1))].addLayout(new_hbox)

        # now to stuff it with filler lines, just so it looks cool :)

        vacuous_lines_needed = len(self.attributes)%10
        for number in range(vacuous_lines_needed):
            vacuous_label = QtWidgets.QLabel()

            vacuous_hBox = QtWidgets.QHBoxLayout()
            vacuous_hBox.addStretch()
            vacuous_hBox.addWidget(vacuous_label)
            vacuous_hBox.addStretch()

            vacuous_label2 = QtWidgets.QLabel()

            vacuous_lhBox = QtWidgets.QHBoxLayout()
            vacuous_lhBox.addStretch()
            vacuous_lhBox.addWidget(vacuous_label2)
            vacuous_lhBox.addStretch()



            column_map[("column"+str(number_of_columns-2))].addLayout(vacuous_lhBox)
            column_map[(("column"+str(number_of_columns-1)))].addLayout(vacuous_hBox)

        for key in column_map:
            self.grand_hbox.addLayout(column_map[key])
        self.setLayout(self.grand_hbox)


            ## this next line will probably need a little changing ; the implication structure should depend on the inventory
        self.implication_structure = {('high1',True):('low',False),('low1',True):('high',False),('front1',True):('back',False),('back1',True):('front',False),
                                      ('approximant1',True):('sonorant',True),
                                      ('syllabic2',True):('constrG',False),('sonorant1',True):('constrG',False),
                                      ('approximant2',True):('constrG',False),('voice1',True):('constrG',False),
                                      ('spreadG1',True):('constrG',False),('continuant1',True):('constrG',False),
                                      ('constrG1',True):('spreadG',False),('lateral1',True):('consonantal',True),
                                      ('delR1',True):('consonantal',True),('delR2',True):('syllabic',False),
                                      ('delR3', True): ('sonorant', False),('delR4',True):('approximant',False),
                                      ('delR5',True):('nasal',False),('delR6', True): ('round', False),
                                      ('delR7',True):('atr',None),('nasal1',True):('sonorant',True),
                                      ('nasal2',True):('approximant',False),('nasal3',True):('lateral',False),
                                      ('nasal4',True):('delR',False),('nasal5',True):('strident',False),
                                      ('labial',True):('coronal',False),('coronal1',True):('consonantal',True),
                                      ('coronal2',True):('labial',False),('coronal3',True):('round',False),
                                      ('coronal4',False):('anterior',None),('anterior1',True):('coronal',True),('anterior2',False):('coronal',True),
                                      ('distributed',True):('consonantal',True),('strident',True):('delR',True),
                                      ('dorsal1',False):('high',None),('dorsal2', False): ('low', None),
                                      ('dorsal3',False):('front',None),('dorsal4',False):('back',None),
                                      ('dorsal5',False):('atr',None),('high2',True):('dorsal',True),
                                      ('low2',True):('dorsal',True),('front2',True):('dorsal',True),
                                      ('back2',True):('dorsal',True),('atr1',True):('dorsal',True),
                                      ('high3', False): ('dorsal', True), ('low3', False): ('dorsal', True),
                                      ('front3', False): ('dorsal', True), ('back3', False): ('dorsal', True),
                                      ('atr2', False): ('dorsal', True),}

        self.setWindowTitle('Phoneme Builder')
        self.show()

    def show_assistive_click(self):
        self.asistive_click_window =assistive_click(self,self.import_line,self.chosenInventory,"All Phonemes",True,self.import_btn)

    """
    def update_language_list(self):
        for number in range(len(self.languages)):
            self.chooseLanguage.removeItem(1)
        if self.chooseInventory.currentText() == "Null" or self.chooseInventory.currentText() == None:
            hey_man = QtWidgets.QMessageBox.warning(self,"Pick an Inventory First!","You need to pick a feature set inventory first",QMessageBox.Ok)
            return None
        sound_set = self.chooseInventory.currentText()
        for item in set_map[sound_set]:
            self.chooseLanguage.addItem(item)
            if item not in self.languages:
                self.languages.append(item)
    """
    def save_phoneme(self): ### Make it so that you can overwrite, you prolly need ta fix smth
        def booleanify(text):
            answer = None
            if text == 'Null':
                answer = None
            elif text == 'True':
                answer = True
            elif text == 'False':
                answer= False
            else:
                answer = None
            return answer
        target_inventory = self.chooseInventory.currentText()
        new_phoneme_name = self.save_as_line.text()


        if ' ' in new_phoneme_name or ',' in new_phoneme_name:
            hey_man = QtWidgets.QMessageBox.information(self,'Invalid Name','Sorry, No Spaces or Commas are Allowed in Phoneme Names!',QMessageBox.Ok)
        elif new_phoneme_name == "":
            hey_man = QtWidgets.QMessageBox.information(self, 'Name Required',
                                                        'Choose a Name or a Symbol for the New Phoneme',
                                                        QMessageBox.Ok)
        else:
            if new_phoneme_name in inventories[self.chosenInventory]["All Phonemes"]:
                hey_man = QtWidgets.QMessageBox.question(self, 'Overwrite Phoneme?',
                                                            'There\'s Already a Phoneme with that Name! If You Go Forward You Will Overwrite the Old Value. \n Do you Wish to Continue?',
                                                            QMessageBox.Yes|QMessageBox.No)
                if hey_man==QMessageBox.No:
                    return False
                else:
                    pass
            definition_of_phoneme = [new_phoneme_name]
            #phoneme_value_map = {'name':None}
            kwargsDict = {}
            for key in self.value_map:
                kwargsDict[key] = booleanify(self.value_map[key].text())
            #
            for key in kwargsDict:
                definition_of_phoneme.append(kwargsDict[key])
            """new_phoneme = phoneme(definition_of_phoneme[0], definition_of_phoneme[1], definition_of_phoneme[2], definition_of_phoneme[3], definition_of_phoneme[4], definition_of_phoneme[5], definition_of_phoneme[6],
                                  definition_of_phoneme[7], definition_of_phoneme[8], definition_of_phoneme[9], definition_of_phoneme[10], definition_of_phoneme[11], definition_of_phoneme[12],
                                  definition_of_phoneme[13], definition_of_phoneme[14], definition_of_phoneme[15], definition_of_phoneme[16], definition_of_phoneme[17], definition_of_phoneme[18],
                                  definition_of_phoneme[19], definition_of_phoneme[20], definition_of_phoneme[21], definition_of_phoneme[22], definition_of_phoneme[23])"""

            #phoneme_value_map['name']= new_phoneme_name
            new_phoneme = feature_set_class_map[self.chosenInventory](**kwargsDict)
            new_phoneme.name = new_phoneme_name
            
            kwargsDict['name']=new_phoneme_name
            ### Ok now we have made the phoneme! now it's time to repackage it for saving purposes. TBH, the line
            ### of code above is probably not necessary, I'm just being honest.
            packaged_version = []
            for key in kwargsDict:
                packaged_version.append((key,kwargsDict[key]))
            packaged_version = tuple(packaged_version)

            global dictionish

            ## removing any copies first
            for possible_copy in dictionish[self.chosenInventory]:
                
                redundant_phoneme = None
                redundant_phoneme_name = None
                for possible_copy_attribute in possible_copy:
                    if possible_copy_attribute[0] == "name" and possible_copy_attribute[1] == new_phoneme_name:
                        redundant_phoneme = possible_copy
                        redundant_phoneme_name = possible_copy_attribute[1]
                if redundant_phoneme != None:
                    dictionish[self.chosenInventory] = [a for a in dictionish[self.chosenInventory] if a != redundant_phoneme]
                    for sub_inventory in inventories[self.chosenInventory]:
                        inventories[self.chosenInventory][sub_inventory] = [a for a in inventories[self.chosenInventory][sub_inventory] if a != redundant_phoneme_name]
                        
            dictionish[self.chosenInventory].append(packaged_version)
            inventories[self.chosenInventory]["All Phonemes"].append(new_phoneme_name)
            print (dictionish)
            #new_phoneme.list_features()

            #!!!!! You prolly want this back TBH
            #set_map[self.chosenInventory]["All Phonemes"].append(new_phoneme)
            
            added_new_sound.set_off()
            if 1 == 1:
                pass
            else:
                pass
            
            if target_inventory in set_map[self.chosenInventory] and target_inventory != "All Phonemes":
                inventories[self.chosenInventory][target_inventory].append(new_phoneme_name)
                set_map[self.chosenInventory][target_inventory].append(new_phoneme)
                hey_man = QtWidgets.QMessageBox.question(self,'Added!','Phoneme Named %s Added to the %s Inventory'%(new_phoneme.name,target_inventory),QMessageBox.Ok)
            else:
                hey_man = QtWidgets.QMessageBox.question(self, 'Added!', 'Phoneme Named %s Added to General Phoneme Inventory'%(new_phoneme.name),
                                                         QMessageBox.Ok)

    # you're gonna have to change this a little ,so that in the data structure, one feature will map on to multiple
    # entailments instead of doing them one at a time.

    def recursive_assume(self,the_sender = None):
        
        
        if self.feature_assumption_toggle.isChecked():

            for impKey in technical_map[self.chosenInventory]["Entailments"]:
                
                it_could_apply = True
                iteration = 0
                while it_could_apply and iteration < len(impKey):
                    comparative_value =""
                    if self.value_map[impKey[iteration][0]].text() == "Null":
                        comparative_value = 'None'
                    else:
                        comparative_value = self.value_map[impKey[iteration][0]].text()

                    if comparative_value != str(impKey[iteration][1]):
                        
                        it_could_apply = False
                    iteration+=1
                
                if it_could_apply:
                    it_does_apply = True
                else:
                    it_does_apply = False
                if it_does_apply:

                    #We have to define the variables in two steps because of an ambiguity in python;
                    # if a tuple is a key in a dictionary to an iterable thing, it picks the wrong things.

                    ## this half of the code executes the necessary changes. the previous half is identifying if u need to do anything

                    questioned_features = technical_map[self.chosenInventory]["Entailments"][impKey]
                    
                    # questioned eatures is a tuple of tuples

                    for questioned_feature in questioned_features:

                        

                        consequent_feature_value = str(questioned_feature[1])
                        
                        current_feature_value = self.value_map[questioned_feature[0]].text()
                        
                        #questioned feature is the one that should get changed - in this case, sonorancy
                        #consequent feature value is what sonarancy should have, and current feature value is what it does currently have.
                        if current_feature_value == "Null":
                            current_feature_value="None"
                        if consequent_feature_value != current_feature_value:
                            if consequent_feature_value == 'True' or consequent_feature_value == 'False':
                                self.value_map[questioned_feature[0]].setText(consequent_feature_value)
                            elif consequent_feature_value == 'None':
                                self.value_map[questioned_feature[0]].setText('Null')
                            colorswab = self.color_map[questioned_feature[0]]
                            if consequent_feature_value == 'None':
                                colorswab.setPixmap(QtGui.QPixmap('pictures/grey.png'))
                            elif consequent_feature_value == 'True':
                                colorswab.setPixmap(QtGui.QPixmap('pictures/green.png'))
                            elif consequent_feature_value == 'False':
                                colorswab.setPixmap(QtGui.QPixmap('pictures/red.png'))
                            did_it_go = True
                        
                        

                        ## use this to find out if the sender was the one who got changed... incomplete
                        the_senders_attribute = None
                        if the_sender != None and isinstance(the_sender,QtWidgets.QPushButton):
                            for attribute in self.value_map:
                                if self.value_map[attribute] == the_sender:
                                    the_senders_attribute = attribute
                                    break
                            
                            
                            
                            ## what's going on here, is the_sender's text is it's null/+/- value, not it's attribute
                            if questioned_feature[0] == the_senders_attribute:
                                implying_statement = ""
                                for number in range(len(impKey)):
                                    if number == len(impKey) -1 and number > 0:
                                        implying_statement += "and "
                                    if impKey[number][1] == True:
                                        implying_statement += "+ "
                                    elif impKey[number][1] == False:
                                        implying_statement += "- "
                                    elif impKey[number][1] == None:
                                        implying_statement += "Null "
                                    implying_statement += impKey[number][0]
                                    if number < len(impKey)-2:
                                        implying_statement += ", "
                                    else:
                                        implying_statement += " "
                                    if len(impKey) == 1:
                                        implying_statement += "entails "
                                    else:
                                        implying_statement += "entail "

                                hey_man = QMessageBox.warning(self, "Cannot Change", "%s that the %s feature must have it's current value."%(implying_statement,the_senders_attribute),
                                                              QMessageBox.Ok)

                # this recursivity may not be needed

        else:
            pass

    def recursive_assume_old(self):
        
        if self.feature_assumption_toggle.isChecked():
            did_it_go=False
            for key in self.value_map:
                
                
                for impKey in technical_map[self.chosenInventory]["Entailments"]:
                    
                    

                    if key in impKey[0]:
                        
                        if self.value_map[key].text() == str(impKey[1]):
                            
                            #We have to define the variables in two steps because of an ambiguity in python;
                            # if a tuple is a key in a dictionary to an iterable thing, it picks the wrong things.
                            questioned_features = technical_map[self.chosenInventory]["Entailments"][impKey]
                            # questioned eatures is a tuple of tuples

                            for questioned_feature in questioned_features:

                                

                                consequent_feature_value = str(questioned_feature[1])
                                
                                current_feature_value = self.value_map[questioned_feature[0]].text()
                                
                                #questioned feature is the one that should get changed - in this case, sonorancy
                                #consequent feature value is what sonarancy should have, and current feature value is what it does currently have.
                                if current_feature_value == "Null":
                                    current_feature_value="None"
                                if consequent_feature_value != current_feature_value:
                                    if consequent_feature_value == 'True' or consequent_feature_value == 'False':
                                        self.value_map[questioned_feature[0]].setText(consequent_feature_value)
                                    elif consequent_feature_value == 'None':
                                        self.value_map[questioned_feature[0]].setText('Null')
                                    colorswab = self.color_map[questioned_feature[0]]
                                    if consequent_feature_value == 'None':
                                        colorswab.setPixmap(QtGui.QPixmap('pictures/grey.png'))
                                    elif consequent_feature_value == 'True':
                                        colorswab.setPixmap(QtGui.QPixmap('pictures/green.png'))
                                    elif consequent_feature_value == 'False':
                                        colorswab.setPixmap(QtGui.QPixmap('pictures/red.png'))
                                    did_it_go = True

                if did_it_go == True:
                    self.recursive_assume()
                else:
                    pass
        else:
            pass

    def assumption_exec(self):
        def assumption(beclicked):
            did_it_go=False
            sender = beclicked
            # OK, I'll be honest, the need for this next line of code defining key is a little weird.
            # without it, the program will still work properly but one of the threads will run an error saying
            # that key is referenced before its assignment. I have no idea why.
            key = 'consonantal'
            for attribute in self.value_map:
                if self.value_map[attribute] == sender:
                    key = attribute
                    break
            for impKey in technical_map[self.chosenInventory]["Entailments"]:
                if key in impKey[0]:

                    if self.value_map[key].text() == str(impKey[1]):
                        questioned_features = technical_map[self.chosenInventory]["Entailments"][impKey]
                        for questioned_feature in questioned_features:
                            consequent_feature_value = str(questioned_feature[1])
                            if consequent_feature_value != self.value_map[questioned_feature[0]].text():
                                if consequent_feature_value == 'True'or consequent_feature_value == 'False':
                                    self.value_map[questioned_feature[0]].setText(consequent_feature_value)
                                elif consequent_feature_value == 'None':
                                    self.value_map[questioned_feature[0]].setText('Null')
                                colorswab = self.color_map[questioned_feature[0]]
                                if consequent_feature_value == 'None':
                                    colorswab.setPixmap(QtGui.QPixmap('pictures/grey.png'))
                                elif consequent_feature_value == 'True':
                                    colorswab.setPixmap(QtGui.QPixmap('pictures/green.png'))
                                elif consequent_feature_value == 'False':
                                    colorswab.setPixmap(QtGui.QPixmap('pictures/red.png'))
                                did_it_go= True

            if did_it_go == True:
                assumption(self.sender())
            else:
                pass
        if self.feature_assumption_toggle.isChecked():
            timer = Timer(2, assumption, [self.sender()])
            timer.start()
        else:
            pass

    def alter_value(self):
        sender = self.sender()
        for key in self.value_map:
            if self.value_map[key] == sender:
                color_label = self.color_map[key]
        if sender.text() == 'Null':
            sender.setText('True')
            color_label.setPixmap(QtGui.QPixmap('pictures/green.png'))
        elif sender.text() == 'True':
            sender.setText('False')
            color_label.setPixmap(QtGui.QPixmap('pictures/red.png'))
        elif sender.text() == 'False':
            sender.setText('Null')
            color_label.setPixmap(QtGui.QPixmap('pictures/grey.png'))

    def populate_phoneme(self):
        """
        if self.chooseFeatureSet.currentText() == "Null":
            hey_man = QMessageBox.warning(self, "Pick a Feature Set Inventory!", "You Need to Pick a Feature Set First!",
                                          QMessageBox.Ok)
            return None"""

        text = self.import_line.text()
        text = re.sub(' ','',text)
        
        chosen_phoneme = None
        if text == ' 'or text =='':
            hey_man = QMessageBox.warning(self, "Pick a Phoneme First!", "You Need to Pick a Phoneme First!", QMessageBox.Ok)

        elif text not in inventories[self.chosenInventory]["All Phonemes"]:
            hey_man = QMessageBox.warning(self, "Phoneme Not Found", "That Phoneme Doesn't Exist", QMessageBox.Ok)
        else:

            for object in set_map[self.chosenInventory]["All Phonemes"]:
                
                
                if object.name == text:
                    
                    chosen_phoneme = object
            
            
            attributes = [a for a in chosen_phoneme.attributes]
            attributes = [a for a in attributes if a != "name"]
            
            for attribute in attributes:
                value = getattr(chosen_phoneme, attribute)
                if value == True:
                    self.value_map[attribute].setText('True')
                    self.color_map[attribute].setPixmap(QtGui.QPixmap("pictures/green.png"))
                elif value == False:
                    self.value_map[attribute].setText('False')
                    self.color_map[attribute].setPixmap(QtGui.QPixmap("pictures/red.png"))
                else:
                    self.value_map[attribute].setText('Null')
                    self.color_map[attribute].setPixmap(QtGui.QPixmap("pictures/grey.png"))


    def update_language_list(self):
        for language in inventories[self.chosenInventory]:
            self.chooseInventory.addItem(language)

    def is_in_tuple(self,candidate,tuple):
        for undertuple in tuple:
            if undertuple[0] == candidate:
                return True
        return False


    def remove_comma(self,target):
        target.setText(re.sub(",","",target.text()))

    """
    def update_inventory_list(self):
        for number in range(len(self.inventories)):
            self.chooseInventory.removeItem(1)

        for item in set_map:
            self.chooseFeatureSet.addItem(item)
            if item not in self.inventories:
                self.inventories.append(item)
                """
class symbol_palette(QtWidgets.QTextEdit):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QtGui.QIcon('pictures/palette.png'))
        self.setStyleSheet("background-color: %s;"%light_brown.name())
        self.setReadOnly(True)
        self.setFontPointSize(12)
        self.append("High vowels: \n ɨ ʉ ɯ")
        self.append("mid vowels: \n ɣ ɵ ɘ ə ø ɛ œ ʌ ɜ ɞ ɔ ɐ")
        self.append("low vowels: \n ɑ ɒ æ Œ")
        self.append("lax vowels: \n ʊ ɪ ʏ")
        self.append("Nasals: \n ŋ ɳ ɲ ɱ")
        self.append("retroflex: \n ɽ ɻ ʐ ʈ ʂ ɖ ɭ ɹ")
        self.append("fricatives and Affricates: \n ʝ ʒ ʤ ʧ ɸ ð ʃ ɣ ʁ ɕ ç θ β")
        self.append("Approximants: \n ɹ ʋ λ ɰ")
        self.append("Taps, Trills, and Others: \n ʙ ɦ ɬ ɫ ɴ ʀ ʔ ʕ ħ ɉ ⱱ ɾ ɧ")
        self.append("Diacritics:\n ʱ ʰ ʷ ʲ ː ˀ ˁ ˔ ˕ ˖ ̙  ̘   ˠ ˥ ˦ ˧ ˨ ˩  ̪  ˽ ̴  ʬ")
        self.setWindowTitle("IPA Symbol Palette")
        self.setGeometry(200,200,400,550)
        self.show()
class answer_display(QtWidgets.QTextEdit):
    def __init__(self):
        super().__init__()
        self.init_ui
    def init_ui(self):
        self.setReadOnly(True)
        self.setGeometry(200,400,200,200)
        self.setFontPointSize(12)


### this under-here-lying class is intended to go unused.
class build_featureset_stack(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__(parent=None)
        self.init_ui()
    def init_ui(self):
        self.page1 = build_featureset(self)
        self.page2 = make_feature_groups(self.page1)
        self.page3 = make_implications(self.page1)
        self.page4 = finalize_featureset(self.page1)
        self.answers = answer_display()
        self.palette = symbol_palette()
        self.addWidget(self.page1)
        self.addWidget(self.page2)
        self.addWidget(self.page3)
        self.addWidget(self.page4)
        self.addWidget(self.answers)
        self.addWidget(self.palette)
        self.setWindowTitle("Create Feature-Set")
        self.setCurrentWidget(self.page1)
        self.show()

        ## for saving stuff
        self.feature_groups = {}

class build_featureset(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.init_ui()
    def init_ui(self):

        ### other pages
        self.page2 = make_feature_groups(self)
        self.page3 = make_implications(self)
        self.page4 = finalize_featureset(self)

        ## for saving
        self.feature_groups = {}
        self.setMinimumWidth(600)
        self.setMinimumHeight(200)

        ## top box ; maybe just forget it?
        """
        self.top_box = QtWidgets.QHBoxLayout()
        self.top_box_left = QtWidgets.QVBoxLayout()
        self.top_box_right = QtWidgets.QVBoxLayout()

        self.added_features_label = QtWidgets.QLabel("Features Added so Far")
        self.top_box_right.addWidget(self.added_features_label)
        self.add_and_import_label = QtWidgets.QLabel("Build Featureset")
        """
        # left column stuff
        self.chooseFeatureSet_label = QtWidgets.QLabel("Select an Inventory to Import from")
        self.chooseFeatureSet = QtWidgets.QComboBox()
        self.chooseFeatureSet.setStyleSheet("background-color: white;")
        self.import_btn = QtWidgets.QPushButton("Import")
        self.import_btn.setStyleSheet("background-color: %s;"%light_teal.name())

        self.save_as_label = QtWidgets.QLabel("Choose a Name")
        self.save_as_line = QtWidgets.QLineEdit()
        self.save_as_line.setStyleSheet("background-color: white;")
        self.save_btn = QtWidgets.QPushButton()
        self.save_btn.setIcon(QtGui.QIcon('pictures/Next Arrow.png'))
        self.save_btn.setText("            Next")
        self.save_btn.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.save_btn.setFixedHeight(30)
        self.save_btn.setIconSize(QtCore.QSize(40,25))
        self.save_btn.setStyleSheet("background-color: %s;"%light_orange.name())

        #!!!!!!!!!
        self.add_feature_label = QtWidgets.QPushButton("Add a Feature")
        self.add_feature_label.setStyleSheet("background-color: %s;"%light_gray.name())
        self.invisi_label = QtWidgets.QLabel()
        self.add_feature_as = QtWidgets.QLineEdit()
        self.add_feature_as.setStyleSheet("background-color: white;")

        self.window_size = 0

        self.leftColumn = QtWidgets.QVBoxLayout()
        self.leftColumn.addWidget(self.chooseFeatureSet_label)
        self.leftColumn.addWidget(self.chooseFeatureSet)
        self.leftColumn.addWidget(self.import_btn)
        #self.leftColumn.addWidget(self.save_as_label)
        #self.leftColumn.addWidget(self.save_as_line)
        self.leftColumn.addWidget(self.add_feature_as)
        self.leftColumn.addWidget(self.add_feature_label)
        self.leftColumn.addWidget(self.invisi_label)
        self.leftColumn.addWidget(self.save_btn)
        # this little bit of gymnastics allows me to set the width of the column that the vBox is.

       # self.Vwidth_widget = QtWidgets.QWidget()
        #self.Vwidth_widget.setLayout(self.leftColumn)
        #self.Vwidth_widget.setFixedWidth(200)
        self.left_column_hbox = QtWidgets.QHBoxLayout()
        self.left_column_hbox.addLayout(self.leftColumn)
        self.left_column_hbox.addStretch(1)

        ## now the frame
        self.left_frame = QtWidgets.QFrame()

        self.left_frame.setStyleSheet("background-color: %s;"%light_green.name())
        self.left_frame.setFrameShape(QFrame.StyledPanel)

        subVbox = QtWidgets.QVBoxLayout(self.left_frame)
        subVbox.addLayout(self.left_column_hbox)
        subVbox.addStretch(1)


        # right column stuff


        self.rightColumnOuter = QtWidgets.QHBoxLayout()

        self.rightColumnInner = QtWidgets.QVBoxLayout()
        self.rightColumnInner.addStretch(1)
        self.widgetCount = 0
        self.appendable_column = self.rightColumnInner

        self.buttonColumnMap ={}

        rightColumn = QtWidgets.QVBoxLayout()



        self.rightColumnOuter.addLayout(self.rightColumnInner)

        rightColumn.addLayout(self.rightColumnOuter)


        grandBox = QtWidgets.QHBoxLayout()
        #grandBox.addLayout(subVbox)
        grandBox.addWidget(self.left_frame)
        #!!! add qframe widget

        # to create a lttle space between the two. I'm sorry if this looks barbaric.
        spacer_column  = QtWidgets.QVBoxLayout()
        self.invisi_label_2 = QtWidgets.QLabel()
        self.invisi_label_2.setMinimumWidth(50)
        spacer_column.addWidget(self.invisi_label_2)

        grandBox.addLayout(spacer_column)
        grandBox.addLayout(rightColumn)
        ### more gymnastics -_-

        granderHbox = QtWidgets.QHBoxLayout()
        granderHbox.addLayout(grandBox)
        granderHbox.addStretch(1)


        ## Feature set selection
        self.inventories = [a for a in feature_set_map]
        self.chooseFeatureSet.setDuplicatesEnabled(False)
        self.chooseFeatureSet.addItem('Null')
        self.update_inventory_list()
        self.chosenInventory = 'Null'

        # this keeps track of how many attributes are out there, so when we got to save we know what to save
        self.current_attributes = []


        self.add_feature_label.clicked.connect(self.add_feature)
        self.import_btn.clicked.connect(self.import_features)
        self.save_btn.clicked.connect(self.next_page)
        self.setLayout(granderHbox)
        self.setWindowTitle("Select Features")
        self.setWindowIcon(QtGui.QIcon('pictures/feature sets.png'))
        self.setMinimumWidth(812)
        self.show()


        # keepin track of stuff

    def add_feature(self):
        if self.add_feature_as.text() == "":
            pass
        else:
            text = self.add_feature_as.text()
            ## normalizing the input, trimming off any excess spaces
            text = text.lower()
            trim = True
            while trim:
                trim = False
                if text[len(text)-1] == ' ':
                    text = text[0:len(text)-1]
                    trim = True

            if text in self.current_attributes:
                
                hey_man = QtWidgets.QMessageBox.warning(self,"Feature Already Present","You've already added this feature. No redundancy allowed.",QMessageBox.Ok)
            else:
                
                new_button = QtWidgets.QPushButton(text)
                new_button.setFixedWidth(100)
                new_button.setToolTip("Click to Delete")

                ## if the number gets to big, we should change columns
                if self.widgetCount == 7:
                    self.widgetCount =0
                    self.new_layout = QtWidgets.QVBoxLayout()
                    self.new_layout.addStretch(1)
                    self.rightColumnOuter.addLayout(self.new_layout)
                    self.appendable_column = self.new_layout

                self.current_attributes.append(text)
                self.appendable_column.addWidget(new_button)
                self.buttonColumnMap[new_button] = self.appendable_column
                new_button.clicked.connect(partial(self.remove_feature,new_button))
                inventory_update.trigger.connect(self.update_inventory_list)

                ## you need to at clicking functionality here

                self.show()



                self.widgetCount += 1
    def remove_feature(self,button):
        
        self.current_attributes = [a for a in self.current_attributes if a != button.text()]
        button.hide()
        self.buttonColumnMap[button].removeWidget(button)
        self.show()
    def update_inventory_list(self):
       # I'm not sure If I need these two lines of code, or if they are just relics kuz i copied them over
       # from the build phoneme widget
       # for number in range(len(self.inventories)):
        #    self.chooseInventory.removeItem(1)

        for item in feature_set_map:
            self.chooseFeatureSet.addItem(item)
            if item not in self.inventories:
                self.inventories.append(item)
    def import_features(self):
        self.chosenInventory = self.chooseFeatureSet.currentText()
        if self.chosenInventory == "Null":
            hey_man = QtWidgets.QMessageBox.warning(self, "Select an Inventory", "You Must Select a Featureset Inventory First",QMessageBox.Ok)
        #if self.chosenInventory == self.chooseFeatureSet.currentText():
        #    return

        # I think I defined an .attributes function


        if self.chosenInventory != 'Null':
            for button in self.buttonColumnMap:
                self.widgetCount = 0
                button.hide()
                self.buttonColumnMap[button].removeWidget(button)

                #self.buttonColumnMap[button].setParent(None)
                self.current_attributes = [a for a in self.current_attributes if a != button.text()]
                self.show()

            ### This could cause issues
            #self.attributes = [a for a in set_map[self.chosenInventory]["All Phonemes"][0].attributes]
            self.attributes = [a for a in feature_set_map[self.chosenInventory] if a != "Name"]
            self.attributes = [a for a in self.attributes if a != "name"]
            for attribute in self.attributes:
                self.add_feature_as.setText(attribute)
                self.add_feature()
            self.add_feature_as.setText('')
    ### This next method prolly shouldn't be here
    def save_feature_set(self):

        ### I think this is an uneccessary bit of code , TBH, this method definition gets repeated :(

        name = self.save_as_line.text()
        attributes = [a for a in self.current_attributes]
        new_class = class_creator(name,attributes)
        # this list of tuples is what will get saved for later. then we can have the machine just dynamically
        # create all the classes at startup.
        #class_tuples.append((name,attributes))
        feature_set_map[name]=attributes
        technical_map[name]={}
        technical_map[name]["keyCategories"] = {}
        set_map[name] = {"All Phonemes":[]}
        inventory_update.set_off()

    def next_page(self):

        if len(self.current_attributes) < 1:
            hey_man = QtWidgets.QMessageBox.warning(self, "More Features Required",
                                                    "You Need to Pick Some Attributes First",
                                                    QMessageBox.Ok)
        else:
            self.hide()
            self.page2.attributes = [a for a in self.current_attributes]
            self.page2.init_ui()
            self.page3.init_ui()
            #self.setCurrentWidget(self.parent.page2)
            #self.setWindowTitle("Create Core Natural Classes")
            self.page2.fill_it_all_out()
            self.page2.setWindowTitle("Define the Primary Feature-Groups")


"""

class make_feature_groups(QMainWindow):
    def __init__(self,parent = None):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.pick_group_features = subordinate_make_feature_groups(self.parent.page1,)
        self.l
        self.right_dock = QtWidgets.QDockWidget('Answers')
        self.addDockWidget(Qt.RightDockWidgetArea, self.right_dock)
        #self.setCentralWidget(self.pick_group_features)
        """

class make_feature_groups(QtWidgets.QWidget):
        def __init__(self,brother=None):
            super().__init__()
            self.brother = brother

            #self.attributes = self.brother.current_attributes
            #self.init_ui()
        def init_ui(self):
            # migh need to do more here
            # do you need to do fill it all out when inintializing?



            self.value_map = {}
            self.color_map = {}
            self.grander_hbox = QtWidgets.QHBoxLayout()
            self.grander_hbox.addStretch()
            self.grand_hbox = QtWidgets.QHBoxLayout()
            self.grand_hbox.addStretch()

            self.save_label = QtWidgets.QLabel("Choose a Name for the Group")

            self.save_btn = QtWidgets.QPushButton("           Add Group")
            self.save_btn.setStyleSheet("background-color: white;")
            self.save_btn.setIcon(QtGui.QIcon('pictures/plus sign.png'))
            #self.save_btn.setText("            Next")
            self.save_btn.setLayoutDirection(QtCore.Qt.RightToLeft)
            #self.save_btn.setFixedHeight(30)
            self.save_btn.setIconSize(QtCore.QSize(40, 25))

            self.next_btn = QtWidgets.QPushButton("             Next")
            self.next_btn.setStyleSheet("background-color: %s;"%light_gray.name())
            self.next_btn.setIcon(QtGui.QIcon('pictures/Next Arrow.png'))
            #self.next_btn.setText("            Next")
            self.next_btn.setLayoutDirection(QtCore.Qt.RightToLeft)
            #self.next_btn.setFixedHeight(30)
            self.next_btn.setIconSize(QtCore.QSize(40, 25))

            self.back_btn = QtWidgets.QPushButton("             Back")
            self.back_btn.setStyleSheet("background-color: %s;"%light_gray.name())
            self.back_btn.setIcon(QtGui.QIcon('pictures/Back arrow.png'))

            self.back_btn.setLayoutDirection(QtCore.Qt.RightToLeft)
            #self.back_btn.setFixedHeight(30)
            self.back_btn.setIconSize(QtCore.QSize(40, 25))

            self.save_btn.setFixedWidth(200)
            self.save_btn.setFixedHeight(50)
            self.next_btn.setFixedWidth(200)
            self.next_btn.setFixedHeight(30)
            self.back_btn.setFixedWidth(200)
            self.back_btn.setFixedHeight(30)
            self.save_as = QtWidgets.QLineEdit()
            self.save_as.setStyleSheet("background-color: white;")
            self.save_as.setFixedWidth(200)

            self.right_side_frame = QFrame()

            self.right_side_frame.setStyleSheet("background-color: %s;"%light_yellow.name())
            self.right_side_frame.setFrameShape(QFrame.StyledPanel)

            self.right_side = QtWidgets.QVBoxLayout(self.right_side_frame)
            self.right_side.addWidget(self.save_label)
            self.right_side.addWidget(self.save_as)
            self.right_side.addWidget(self.save_btn)
            self.right_side.addWidget(self.next_btn)
            self.right_side.addWidget(self.back_btn)
            self.right_side.addStretch(1)


            self.righter_side_frame = QFrame()
            self.righter_side_frame.setFrameShape(QFrame.StyledPanel)

            self.righter_side_frame.setStyleSheet("background-color: %s;"%light_orange.name())

            self.righter_side = QtWidgets.QHBoxLayout()
            self.righter_side_vbox2 = QtWidgets.QVBoxLayout(self.righter_side_frame)
            self.righter_side_vbox2.addLayout(self.righter_side)
            self.righter_side_vbox2.addStretch(1)
            self.righter_side_column = QtWidgets.QVBoxLayout()
            self.righter_side.addLayout(self.righter_side_column)
            self.groups_header = QtWidgets.QLabel()
            self.groups_header.setText("Natural Classes Made So Far")
            self.righter_side_column.addWidget(self.groups_header)
            self.righter_side_column.addStretch(0)
            self.grander_hbox.addLayout(self.grand_hbox)
            #self.grander_hbox.addLayout(self.right_side)
            self.right_side_2 = QtWidgets.QVBoxLayout()
            self.right_side_2.addWidget(self.right_side_frame)
            self.right_side_2.addStretch(1)
            #self.grander_hbox.addWidget(self.right_side_frame)
            self.grander_hbox.addLayout(self.right_side_2)
            #self.grander_hbox.addLayout(self.righter_side)
            self.grander_hbox.addWidget(self.righter_side_frame)
            self.setLayout(self.grander_hbox)

            self.show()
            self.save_btn.clicked.connect(self.add_group)
            self.next_btn.clicked.connect(self.next_page)
            self.back_btn.clicked.connect(self.back_a_page)
            # so that you can delete stuff
            self.button_label_map = {}
            self.button_box_map = {}
            self.button_name_map = {}

            self.group_count = 0
            self.setWindowTitle("Define the Primary Feature-Groups")
            self.setWindowIcon(QtGui.QIcon('pictures/natural classes.png'))
        def next_page(self):

            #self.brother.parent.setCurrentWidget(self.brother.parent.page3)

            #self.brother.parent.setWindowTitle("Make some implications")
            if self.brother.page3.loaded == False:
                self.brother.page3.attributes = [a for a in self.brother.current_attributes]
                self.brother.page3.fill_it_all_out(self.brother.page3.main_col_1_H,True)
                self.brother.page3.fill_it_all_out(self.brother.page3.main_col_3_H,False)
                self.brother.page3.loaded = True
                self.brother.page3.setWindowTitle("Set Entailments for the Featureset")
            self.hide()
            self.brother.page3.show()

        def fill_it_all_out(self,):
            # code for resetting the thing here
            # for luku in range (1,self.grand_hbox.count()):
            #     self.grand_hbox.removeItem(self.grand_hbox.itemAt(luku))
            #     
            #

            #self.chosenInventory = self.chooseFeatureSet.currentText()
            # shouldn't need this next line, kuz self.attributes is alrdy defined.
            #self.attributes = [a for a in self.attributes]

            number_of_columns = 2 * (math.ceil(len(self.attributes) / 10))

            column_map = {}
            self.value_map = {}
            self.color_map = {}
            for number in range(number_of_columns):
                new_col = QtWidgets.QVBoxLayout()
                column_map[("column" + str(number))] = new_col

            # tal is swedish for number
            for tal in range(len(self.attributes)):
                col_no = 2 * (math.floor(tal / 10))

                new_label = QtWidgets.QLabel(self.attributes[tal] + ":")
                new_button = QtWidgets.QPushButton("Null")
                new_pic = QtWidgets.QLabel()
                new_pic.setPixmap(QtGui.QPixmap("pictures/grey.png"))
                new_button.clicked.connect(self.alter_value)
                # this line shouldn't be needed
                #new_button.clicked.connect(self.assumption_exec)

                self.value_map[self.attributes[tal]] = new_button
                self.color_map[self.attributes[tal]] = new_pic

                new_lhbox = QtWidgets.QHBoxLayout()
                new_lhbox.addStretch()
                new_lhbox.addWidget(new_label)
                new_lhbox.addStretch()

                new_hbox = QtWidgets.QHBoxLayout()
                new_hbox.addStretch()
                new_hbox.addWidget(new_button)
                new_hbox.addWidget(new_pic)
                new_hbox.addStretch()

                column_map[("column" + str(col_no))].addLayout(new_lhbox)
                column_map[("column" + str(col_no + 1))].addLayout(new_hbox)

            # now to stuff it with filler lines, just so it looks cool :)

            vacuous_lines_needed = len(self.attributes) % 10
            for number in range(vacuous_lines_needed):
                vacuous_label = QtWidgets.QLabel()

                vacuous_hBox = QtWidgets.QHBoxLayout()
                vacuous_hBox.addStretch()
                vacuous_hBox.addWidget(vacuous_label)
                vacuous_hBox.addStretch()

                vacuous_label2 = QtWidgets.QLabel()

                vacuous_lhBox = QtWidgets.QHBoxLayout()
                vacuous_lhBox.addStretch()
                vacuous_lhBox.addWidget(vacuous_label2)
                vacuous_lhBox.addStretch()

                column_map[("column" + str(number_of_columns - 2))].addLayout(vacuous_lhBox)
                column_map[(("column" + str(number_of_columns - 1)))].addLayout(vacuous_hBox)

            for key in column_map:
                self.grand_hbox.addLayout(column_map[key])
            #self.setLayout(self.grand_hbox)

            ## this next line will probably need a little changing ; the implication structure should depend on the inventory
            self.implication_structure = {('high1', True): ('low', False), ('low1', True): ('high', False),
                                          ('front1', True): ('back', False), ('back1', True): ('front', False),
                                          ('approximant1', True): ('sonorant', True),
                                          ('syllabic2', True): ('constrG', False), ('sonorant1', True): ('constrG', False),
                                          ('approximant2', True): ('constrG', False), ('voice1', True): ('constrG', False),
                                          ('spreadG1', True): ('constrG', False), ('continuant1', True): ('constrG', False),
                                          ('constrG1', True): ('spreadG', False), ('lateral1', True): ('consonantal', True),
                                          ('delR1', True): ('consonantal', True), ('delR2', True): ('syllabic', False),
                                          ('delR3', True): ('sonorant', False), ('delR4', True): ('approximant', False),
                                          ('delR5', True): ('nasal', False), ('delR6', True): ('round', False),
                                          ('delR7', True): ('atr', None), ('nasal1', True): ('sonorant', True),
                                          ('nasal2', True): ('approximant', False), ('nasal3', True): ('lateral', False),
                                          ('nasal4', True): ('delR', False), ('nasal5', True): ('strident', False),
                                          ('labial', True): ('coronal', False), ('coronal1', True): ('consonantal', True),
                                          ('coronal2', True): ('labial', False), ('coronal3', True): ('round', False),
                                          ('coronal4', False): ('anterior', None), ('anterior1', True): ('coronal', True),
                                          ('anterior2', False): ('coronal', True),
                                          ('distributed', True): ('consonantal', True), ('strident', True): ('delR', True),
                                          ('dorsal1', False): ('high', None), ('dorsal2', False): ('low', None),
                                          ('dorsal3', False): ('front', None), ('dorsal4', False): ('back', None),
                                          ('dorsal5', False): ('atr', None), ('high2', True): ('dorsal', True),
                                          ('low2', True): ('dorsal', True), ('front2', True): ('dorsal', True),
                                          ('back2', True): ('dorsal', True), ('atr1', True): ('dorsal', True),
                                          ('high3', False): ('dorsal', True), ('low3', False): ('dorsal', True),
                                          ('front3', False): ('dorsal', True), ('back3', False): ('dorsal', True),
                                          ('atr2', False): ('dorsal', True), }

            self.setWindowTitle('Phoneme Builder')
            self.show()

        def alter_value(self):
            sender = self.sender()
            for key in self.value_map:
                if self.value_map[key] == sender:
                    color_label = self.color_map[key]
            if sender.text() == 'Null':
                sender.setText('True')
                color_label.setPixmap(QtGui.QPixmap('pictures/green.png'))
            elif sender.text() == 'True':
                sender.setText('False')
                color_label.setPixmap(QtGui.QPixmap('pictures/red.png'))
            elif sender.text() == 'False':
                sender.setText('Null')
                color_label.setPixmap(QtGui.QPixmap('pictures/grey.png'))

        def add_group(self):
            ## normalizing the input, trimming off any excess spaces
            
            group_name = self.save_as.text()
            if group_name == "":
                hey_man = QtWidgets.QMessageBox.warning(self, "Name Required!", "You Need to Enter a Name for Your Group First!",
                                                        QMessageBox.Ok)
            else:
                group_name = group_name.lower()
                trim = True
                while trim:
                    trim = False
                    if group_name[len(group_name) - 1] == ' ':
                        group_name = group_name[0:len(group_name) - 1]
                        trim = True
                if group_name == "":
                    hey_man = QtWidgets.QMessageBox.warning(self,"Name Required!","You Need to Enter a Name for Your Group First!",QMessageBox.Ok)
                elif self.group_count > 8:
                    hey_man = QtWidgets.QMessageBox.warning(self, "Too Many Groups", "You just don't need this many groups man, just trust me",
                                                            QMessageBox.Ok)
                else:
                    
                    # making the tuple so that it can be compared
                    group_name = group_name[0].upper() + group_name[1:len(group_name)]
                    list_of_defining_attributes = []
                    label_text = ""
                    label_text += group_name
                    label_text += ": "
                    for key in self.value_map:
                        if self.value_map[key].text() == 'True':
                            label_text += ( " + " + key)
                            new_tuple = (key,True)
                            list_of_defining_attributes.append(new_tuple)
                        elif self.value_map[key].text() == 'False':
                            label_text += (" - "+ key)
                            new_tuple = (key,False)
                            list_of_defining_attributes.append(new_tuple)
                    
                    end_tuple = tuple(list_of_defining_attributes)
                    # another wave of conditions
                    redundant_class = False
                    for group in self.brother.feature_groups:
                        if self.is_the_group_the_same(self.brother.feature_groups[group],end_tuple) == True:
                            redundant_class = True
                    if group_name in self.brother.feature_groups:
                        hey_man = QtWidgets.QMessageBox.warning(self, "The name is taken",
                                                                "You May Not Have Two Groups With One Name",
                                                                QMessageBox.Ok)
                    elif redundant_class == True:
                        hey_man = QtWidgets.QMessageBox.warning(self, "Redundant Group",
                                                                "You Already Have a Group With the Same Features",
                                                                QMessageBox.Ok)
                    elif len(list_of_defining_attributes) == 0:
                        hey_man = QtWidgets.QMessageBox.warning(self, "No Defining Features",
                                                                "Pick Some Features to Define the Group First.",
                                                                QMessageBox.Ok)
                    else:
                        new_horiz_box = QtWidgets.QHBoxLayout()
                        new_label = QtWidgets.QLabel()
                        new_label.setText(label_text)
                        new_label.setWordWrap(True)
                        new_label.setFixedWidth(100)
                        delete_button = QtWidgets.QPushButton()
                        delete_button.setText("Delete")
                        delete_button.setFixedWidth(75)
                        new_horiz_box.addWidget(new_label)
                        new_horiz_box.addWidget(delete_button)
                        self.righter_side_column.addLayout(new_horiz_box)

                        # now making the button removable
                        delete_button.clicked.connect(partial(self.remove_group,delete_button))
                        self.button_label_map[delete_button] = new_label
                        self.button_box_map[delete_button]= new_horiz_box

                        # now we gotta save the group
                        self.brother.feature_groups[group_name]=end_tuple
                        self.button_name_map[delete_button] = group_name
                        self.group_count +=1
        def remove_group(self,button):
            button.hide()
            group_name = self.button_label_map[button]
            self.button_label_map[button].hide()
            ## ?? why do I not need this line? I'm confused. It works well without it, but you'd think that you'd need
            ## to remove the label AND the button. /shrug
            #self.button_box_map[button].removeWidget(button_label_map[button])
            self.button_box_map[button].removeWidget(button)
            self.show()
            self.group_count -= 1

            # now to actually remove the data
            self.brother.feature_groups.pop(self.button_name_map[button],None)
        def back_a_page(self):
            hey_man = QtWidgets.QMessageBox.question(self, 'Going Back To Page 1',
                                                     'Going back to page 1 will erase all your work on pages 2 and 3. Are you sure you want to continue?',
                                                     QMessageBox.Yes | QMessageBox.No)

            if hey_man == QMessageBox.Yes:
                

                self.brother.page4.brother = None
                self.brother.page3.brother = None

                reset2 = make_feature_groups(self.brother)
                reset3 = make_implications(self.brother)
                reset4 = finalize_featureset(self.brother)


                self.brother.feature_groups = {}

                self.brother.page4 = reset4
                self.brother.page3 = reset3
                self.brother.page2 = reset2


                #self.brother.parent.addWidget(self.brother.parent.page2)
                #self.brother.parent.addWidget(self.brother.parent.page3)
                #self.brother.parent.addWidget(self.brother.parent.page4)
                #self.brother.parent.setCurrentWidget(self.brother.parent.page1)
                #self.brother.parent.setWindowTitle("Featureset Builder")
                self.hide()
                self.brother.show()
                self.brother = None
        def is_the_group_the_same(self,tuple_of_tuples_1,tuple_of_tuples_2):
            are_they_the_same = True
            testing_dictionary_1 = {}
            testing_dictionary_1_len = 0
            for tuple in tuple_of_tuples_1:
                testing_dictionary_1[tuple[0]] = tuple[1]
                testing_dictionary_1_len +=1
            testing_dictionary_2 = {}
            testing_dictionary_2_len = 0
            for tuple in tuple_of_tuples_2:
                testing_dictionary_2[tuple[0]] = tuple[1]
                testing_dictionary_2_len += 1
            for key in testing_dictionary_1:
                if key not in testing_dictionary_2:
                    are_they_the_same = False
                elif testing_dictionary_1[key] != testing_dictionary_2[key]:
                    are_they_the_same = False
                elif testing_dictionary_1_len != testing_dictionary_2_len:
                    are_they_the_same = False
                else:
                    pass
            return (are_they_the_same)
class make_implications(QtWidgets.QWidget):
    def __init__(self, brother=None):
        super().__init__()
        self.brother = brother

        #self.attributes = self.brother.current_attributes
        #self.init_ui()
    def init_ui(self):
        # migh need to do more here
        # do you need to do fill it all out when inintializing?

        self.move(215, 279)

        self.col_4_frame = QtWidgets.QFrame()
        self.col_4_frame.setStyleSheet("background-color: %s;"%light_yellow.name())
        self.col_4_frame.setFrameShape(QFrame.StyledPanel)

        self.col_5_frame = QtWidgets.QFrame()
        self.col_5_frame.setStyleSheet("background-color: %s;"%light_orange.name())
        self.col_5_frame.setFrameShape(QFrame.StyledPanel)


        self.loaded = False

        self.value_map = {}
        self.color_map = {}
        self.implier_value_map = {}
        self.implier_color_map = {}
        self.grandest_hbox = QtWidgets.QHBoxLayout()
        self.main_col_1 = QtWidgets.QVBoxLayout()
        self.main_col_1_H = QtWidgets.QHBoxLayout()
        self.main_col_2 = QtWidgets.QVBoxLayout()
        self.main_col_3 = QtWidgets.QVBoxLayout()
        self.main_col_3_H = QtWidgets.QHBoxLayout()
        self.main_col_4 = QtWidgets.QVBoxLayout(self.col_4_frame)
        self.main_col_5 = QtWidgets.QVBoxLayout(self.col_5_frame)
        self.main_col_5_H = QtWidgets.QHBoxLayout()
        self.maincol_5_V = QtWidgets.QVBoxLayout()

        self.main_col_1.addLayout(self.main_col_1_H)
        self.main_col_3.addLayout(self.main_col_3_H)
        self.main_col_5.addLayout(self.main_col_5_H)
        self.main_col_5_H.addLayout(self.maincol_5_V)

        self.grandest_hbox.addLayout(self.main_col_1)
        self.grandest_hbox.addLayout(self.main_col_2)
        self.grandest_hbox.addLayout(self.main_col_3)
        #self.grandest_hbox.addLayout(self.main_col_4)
        #self.grandest_hbox.addLayout(self.main_col_5)
        #self.grandest_hbox.addWidget(self.col_4_frame)
        self.col_4_2 = QtWidgets.QVBoxLayout()
        self.col_4_2.addWidget(self.col_4_frame)
        self.col_4_2.addStretch(1)
        self.grandest_hbox.addLayout(self.col_4_2)

        self.grandest_hbox.addWidget(self.col_5_frame)

        self.implication_arrow = QtWidgets.QLabel()
        self.implication_arrow.setPixmap(QtGui.QPixmap('pictures/Impliesarrow.png'))
        self.main_col_2.addWidget(self.implication_arrow)

        self.add_button = QtWidgets.QPushButton()
        self.add_button.setText("        Add Implication")
        self.add_button.setStyleSheet("background-color: white;")
        self.add_button.setIcon(QtGui.QIcon('pictures/plus sign.png'))
        self.add_button.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.add_button.setIconSize(QtCore.QSize(40, 25))

        self.add_button.clicked.connect(self.add_implication)
        self.add_button.setFixedHeight(50)
        self.add_button.setFixedWidth(200)
        self.next_button = QtWidgets.QPushButton()
        self.next_button.setText("             Next")
        self.next_button.setIcon(QtGui.QIcon('pictures/Next Arrow.png'))
        self.next_button.setStyleSheet("background-color: %s;"%light_gray.name())
        self.next_button.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.next_button.setIconSize(QtCore.QSize(40,25))

        self.next_button.clicked.connect(self.next_page)
        self.next_button.setFixedHeight(30)
        self.next_button.setFixedWidth(200)

        self.back_button = QtWidgets.QPushButton()
        self.back_button.setText("             Back")
        self.back_button.setIcon(QtGui.QIcon('pictures/Back arrow.png'))
        self.back_button.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.back_button.setIconSize(QtCore.QSize(40, 25))
        self.back_button.setStyleSheet("background-color: %s;"%light_gray.name())
        self.back_button.clicked.connect(self.back_a_page)
        self.back_button.setFixedHeight(30)
        self.back_button.setFixedWidth(200)


        self.main_col_4.addWidget(self.add_button)
        self.main_col_4.addWidget(self.next_button)
        self.main_col_4.addWidget(self.back_button)
        self.main_col_4.addStretch(1)

        # tooltips
        self.add_button.setToolTip("Click here to add an entailment")
        self.next_button.setToolTip("Click here to move on to the next step")
        self.back_button.setToolTip("Click here to go back to step 2")




        self.setLayout(self.grandest_hbox)


        # implicationcount allows you to make sure that when you add too many implications, they will
        # form new columns instead of just making one big fat long column.

        self.implication_count = 1
        self.target_box = self.maincol_5_V


        # so you can delete implications:
        self.delete_btn_label_map = {}

        self.entailments_here_label = QtWidgets.QLabel("Entailments added so far:")
        self.target_box.addWidget(self.entailments_here_label)
        self.target_box.addStretch(0)
        self.spacerItem= QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.target_box.addItem(self.spacerItem)

        # so that you can delete stuff
        self.button_label_map = {}
        self.button_box_map = {}
        self.delete_button_to_implier_map = {}

        # Lastly, to save the data.
        self.implications = {}

        self.implications_to_button_map = {}
        self.setWindowTitle("Set Entailments for the Featureset")
        self.setWindowIcon(QtGui.QIcon('pictures/entailments.png'))

    def back_a_page(self):
        #self.brother.parent.setCurrentWidget(self.brother.parent.page2)
        self.hide()
        self.brother.page2.show()
    def fill_it_all_out(self,recipient_box,implier = None):
        # code for resetting the thing here
        # for luku in range (1,self.grand_hbox.count()):
        #     self.grand_hbox.removeItem(self.grand_hbox.itemAt(luku))
        #     
        #

        # self.chosenInventory = self.chooseFeatureSet.currentText()
        # shouldn't need this next line, kuz self.attributes is alrdy defined.
        # self.attributes = [a for a in self.attributes]
        number_of_columns = 2 * (math.ceil(len(self.attributes) / 10))

        column_map = {}
        # you prolly would rather initialize these outside of the function, kuz you're gonna do it twice
        # on this page.
        #self.value_map = {}
        #self.color_map = {}
        for number in range(number_of_columns):
            new_col = QtWidgets.QVBoxLayout()
            column_map[("column" + str(number))] = new_col

        # tal is swedish for number
        for tal in range(len(self.attributes)):
            col_no = 2 * (math.floor(tal / 10))

            new_label = QtWidgets.QLabel(self.attributes[tal] + ":")
            new_button = QtWidgets.QPushButton("-")
            new_pic = QtWidgets.QLabel()
            new_pic.setPixmap(QtGui.QPixmap("pictures/grey.png"))

            # this line shouldn't be needed
            # new_button.clicked.connect(self.assumption_exec)
            if implier == False:
                self.value_map[self.attributes[tal]] = new_button
                self.color_map[self.attributes[tal]] = new_pic
                new_button.clicked.connect(self.alter_value)
            elif implier == True:
                self.implier_value_map[self.attributes[tal]] = new_button
                self.implier_color_map[self.attributes[tal]] = new_pic
                new_button.clicked.connect(self.implier_alter_value)

            new_button.setFixedWidth(40)

            new_lhbox = QtWidgets.QHBoxLayout()
            new_lhbox.addStretch()
            new_lhbox.addWidget(new_label)
            new_lhbox.addStretch()

            new_hbox = QtWidgets.QHBoxLayout()
            new_hbox.addStretch()
            new_hbox.addWidget(new_button)
            new_hbox.addWidget(new_pic)
            new_hbox.addStretch()

            column_map[("column" + str(col_no))].addLayout(new_lhbox)
            column_map[("column" + str(col_no + 1))].addLayout(new_hbox)

        # now to stuff it with filler lines, just so it looks cool :)

        vacuous_lines_needed = len(self.attributes) % 10
        for number in range(vacuous_lines_needed):
            vacuous_label = QtWidgets.QLabel()

            vacuous_hBox = QtWidgets.QHBoxLayout()
            vacuous_hBox.addStretch()
            vacuous_hBox.addWidget(vacuous_label)
            vacuous_hBox.addStretch()

            vacuous_label2 = QtWidgets.QLabel()

            vacuous_lhBox = QtWidgets.QHBoxLayout()
            vacuous_lhBox.addStretch()
            vacuous_lhBox.addWidget(vacuous_label2)
            vacuous_lhBox.addStretch()

            column_map[("column" + str(number_of_columns - 2))].addLayout(vacuous_lhBox)
            column_map[(("column" + str(number_of_columns - 1)))].addLayout(vacuous_hBox)

        for key in column_map:
            recipient_box.addLayout(column_map[key])
        # self.setLayout(self.grand_hbox)

        ## this next line will probably need a little changing ; the implication structure should depend on the inventory
        self.implication_structure = {('high1', True): ('low', False), ('low1', True): ('high', False),
                                      ('front1', True): ('back', False), ('back1', True): ('front', False),
                                      ('approximant1', True): ('sonorant', True),
                                      ('syllabic2', True): ('constrG', False), ('sonorant1', True): ('constrG', False),
                                      ('approximant2', True): ('constrG', False), ('voice1', True): ('constrG', False),
                                      ('spreadG1', True): ('constrG', False), ('continuant1', True): ('constrG', False),
                                      ('constrG1', True): ('spreadG', False), ('lateral1', True): ('consonantal', True),
                                      ('delR1', True): ('consonantal', True), ('delR2', True): ('syllabic', False),
                                      ('delR3', True): ('sonorant', False), ('delR4', True): ('approximant', False),
                                      ('delR5', True): ('nasal', False), ('delR6', True): ('round', False),
                                      ('delR7', True): ('atr', None), ('nasal1', True): ('sonorant', True),
                                      ('nasal2', True): ('approximant', False), ('nasal3', True): ('lateral', False),
                                      ('nasal4', True): ('delR', False), ('nasal5', True): ('strident', False),
                                      ('labial', True): ('coronal', False), ('coronal1', True): ('consonantal', True),
                                      ('coronal2', True): ('labial', False), ('coronal3', True): ('round', False),
                                      ('coronal4', False): ('anterior', None), ('anterior1', True): ('coronal', True),
                                      ('anterior2', False): ('coronal', True),
                                      ('distributed', True): ('consonantal', True), ('strident', True): ('delR', True),
                                      ('dorsal1', False): ('high', None), ('dorsal2', False): ('low', None),
                                      ('dorsal3', False): ('front', None), ('dorsal4', False): ('back', None),
                                      ('dorsal5', False): ('atr', None), ('high2', True): ('dorsal', True),
                                      ('low2', True): ('dorsal', True), ('front2', True): ('dorsal', True),
                                      ('back2', True): ('dorsal', True), ('atr1', True): ('dorsal', True),
                                      ('high3', False): ('dorsal', True), ('low3', False): ('dorsal', True),
                                      ('front3', False): ('dorsal', True), ('back3', False): ('dorsal', True),
                                      ('atr2', False): ('dorsal', True), }

        self.setWindowTitle('Phoneme Builder')
        self.show()

    def alter_value(self):
        sender = self.sender()
        for key in self.value_map:
            if self.value_map[key] == sender:
                color_label = self.color_map[key]
        if sender.text() == '-':
            sender.setText('True')
            color_label.setPixmap(QtGui.QPixmap('pictures/green.png'))
        elif sender.text() == 'True':
            sender.setText('False')
            color_label.setPixmap(QtGui.QPixmap('pictures/red.png'))
        elif sender.text() == 'False':
            sender.setText('Null')
            color_label.setPixmap(QtGui.QPixmap('pictures/yellow.png'))
        elif sender.text() == 'Null':
            sender.setText('-')
            color_label.setPixmap(QtGui.QPixmap('pictures/grey.png'))

    def implier_alter_value(self):
        sender = self.sender()

        ## not the most efficient way of doing this (sigh) but I don't care enough to fix it, lol :) it shouldn't be a problem.
        for key in self.implier_value_map:
            if self.implier_value_map[key] == sender:
                color_label = self.implier_color_map[key]

        if sender.text() == 'Null':
            sender.setText('-')
            color_label.setPixmap(QtGui.QPixmap('pictures/grey.png'))
        elif sender.text() == '-':
            sender.setText("True")
            color_label.setPixmap(QtGui.QPixmap('pictures/green.png'))
        elif sender.text() == 'True':
            sender.setText('False')
            color_label.setPixmap(QtGui.QPixmap('pictures/red.png'))
        elif sender.text() == 'False':
            sender.setText('Null')
            color_label.setPixmap(QtGui.QPixmap('pictures/yellow.png'))
        ### maybe make it so that you can do have null imply..?

    def add_implication(self):

        # list of consequences for saving is final result, that a key tuple gets mapped into inside the self.implications dictionary
        # self.implier_value_map is a dictionary that links an attribute to a button
        #implications to button map maps the implication (namely, the implying tuple) to the label of the right column used to represent it.

        key_tuple = []
        new_label_text = ""
        was_something_changed = False
        for key in self.implier_value_map:
            if self.implier_value_map[key].text() != "-":
                was_something_changed = True
                # What we want as a result, is a tuple of tuples; that is, a key_tuple full of undertuples.
                undertuple = [key]
                if self.implier_value_map[key].text() == "True":
                    #new_label_text += "+ "
                    undertuple.append(True)
                elif self.implier_value_map[key].text() == "False":
                    #new_label_text += "- "
                    undertuple.append(False)
                elif self.implier_value_map[key].text() == "Null":
                    undertuple.append(None)

                undertuple = tuple(undertuple)
                key_tuple.append(undertuple)

        key_tuple = tuple(key_tuple)

        ## starting off the label text.

        for number in range(len(key_tuple)):
            if number == len(key_tuple)-1 and number == 0:
                if key_tuple[number][1] == True:
                    new_label_text += "+ "
                elif key_tuple[number][1] == False:
                    new_label_text +="- "
                elif key_tuple[number][1] == None:
                    new_label_text += "Null "

                new_label_text += key_tuple[number][0]
            elif number == len(key_tuple) - 1:
                new_label_text += "and "
                if key_tuple[number][1] == True:
                    new_label_text += "+ "
                elif key_tuple[number][1] == False:
                    new_label_text += "- "
                elif key_tuple[number][1] == None:
                    new_label_text += "Null "

                new_label_text += key_tuple[number][0]

            elif number == len(key_tuple) - 2:
                if key_tuple[number][1] == True:
                    new_label_text += "+ "
                elif key_tuple[number][1] == False:
                    new_label_text += "- "
                elif key_tuple[number][1] == None:
                    new_label_text += "Null "

                new_label_text += key_tuple[number][0]
                new_label_text += " "


            else:
                if key_tuple[number][1] == True:
                    new_label_text += "+ "
                elif key_tuple[number][1] == False:
                    new_label_text += "- "
                elif key_tuple[number][1] == None:
                    new_label_text += "Null "
                new_label_text += key_tuple[number][0]
                new_label_text += ", "

        if len(key_tuple)>1:
            new_label_text+= " imply: "
        else:
            new_label_text += " implies: "

        list_of_consequences_for_saving = []
        list_of_consequences = []
        was_something_else_changed = False
        for key in self.value_map:
            if self.value_map[key].text() != "-":
                was_something_else_changed = True
                if self.value_map[key].text() == "True":
                    list_of_consequences.append((key,' + '))
                    list_of_consequences_for_saving.append((key,True))
                elif self.value_map[key].text() == "False":
                    list_of_consequences.append((key,' - '))
                    list_of_consequences_for_saving.append((key,False))
                elif self.value_map[key].text() == "Null":
                    list_of_consequences.append((key,' Null '))
                    list_of_consequences_for_saving.append((key,None))

        for number in range(len(list_of_consequences)):
            if len(list_of_consequences)==1:
                new_label_text += list_of_consequences[number][1]
                new_label_text += list_of_consequences[number][0]
                new_label_text += "."
            elif number == len(list_of_consequences)-1:
                new_label_text += " and "
                new_label_text += list_of_consequences[number][1]
                new_label_text += list_of_consequences[number][0]
                new_label_text += "."
            elif number == len(list_of_consequences)-2:
                new_label_text += list_of_consequences[number][1]
                new_label_text += list_of_consequences[number][0]
            else:
                new_label_text += list_of_consequences[number][1]
                new_label_text += list_of_consequences[number][0]
                new_label_text += ","


        if was_something_changed and was_something_else_changed:
            list_of_consequences_for_saving = tuple(list_of_consequences_for_saving)
            if key_tuple in self.implications:
                
                self.implications_to_button_map[key_tuple].setText(new_label_text)
                
                self.implications[key_tuple] = list_of_consequences_for_saving
                
            else:


                new_label = QtWidgets.QLabel()
                new_label.setText(new_label_text)
                delete_btn = QtWidgets.QPushButton()
                delete_btn.setText("Delete")
                new_label.setWordWrap(True)
                delete_btn.setFixedWidth(50)
                new_label.setFixedWidth(200)
                # ok this if statement helps us make new columns when needed.
                if self.implication_count == 10:
                    #reset the count,
                    self.implication_count = 0
                    # then make a new column :)
                    new_column = QtWidgets.QVBoxLayout()
                    self.target_box = new_column
                    self.main_col_5_H.addLayout(self.target_box)
                    self.target_box.addItem(self.spacerItem)
                else:
                    self.implication_count += 1

                new_hori_box = QtWidgets.QHBoxLayout()
                new_hori_box.addWidget(new_label)
                new_hori_box.addWidget(delete_btn)
                self.target_box.removeItem(self.spacerItem)
                self.target_box.addLayout(new_hori_box)
                self.target_box.addItem(self.spacerItem)
                ## just so you can delete stuff:

                self.delete_btn_label_map[delete_btn] = new_label
                self.delete_button_to_implier_map[delete_btn] = key_tuple
                delete_btn.clicked.connect(self.delete_me)
                self.show()
                # we still need to add stuff in so it actually saves tho
                list_of_consequences_for_saving = tuple(list_of_consequences_for_saving)
                self.implications[key_tuple] = list_of_consequences_for_saving
                self.implications_to_button_map[key_tuple]=new_label


    def add_implication_old(self):
        key_tuple = [" ",None]
        new_label_text = ""
        was_something_changed = False
        for key in self.implier_value_map:
            if self.implier_value_map[key].text() != "Null":
                was_something_changed = True
                if self.implier_value_map[key].text() == "True":
                    new_label_text += "+ "
                    key_tuple[1] = True
                elif self.implier_value_map[key].text() == "False":
                    new_label_text += "- "
                    key_tuple[1] = False
                key_tuple[0] = key
                new_label_text += key
                new_label_text += " implies: "
        key_tuple = tuple(key_tuple)
        list_of_consequences_for_saving = []
        list_of_consequences = []
        was_something_else_changed = False
        for key in self.value_map:
            if self.value_map[key].text() != "Null":
                was_something_else_changed = True
                if self.value_map[key].text() == "True":
                    list_of_consequences.append((key,' + '))
                    list_of_consequences_for_saving.append((key,True))
                elif self.value_map[key].text() == "False":
                    list_of_consequences.append((key,' - '))
                    list_of_consequences_for_saving.append((key,False))
        for consequence in list_of_consequences:
            new_label_text += consequence[1]
            new_label_text += consequence[0]

        if was_something_changed and was_something_else_changed:
            list_of_consequences_for_saving = tuple(list_of_consequences_for_saving)
            if key_tuple in self.implications:
                
                self.implications_to_button_map[key_tuple].setText(new_label_text)
                
                self.implications[key_tuple] = list_of_consequences_for_saving
                
            else:


                new_label = QtWidgets.QLabel()
                new_label.setText(new_label_text)
                delete_btn = QtWidgets.QPushButton()
                delete_btn.setText("Delete")
                new_label.setWordWrap(True)
                delete_btn.setFixedWidth(50)
                new_label.setFixedWidth(200)
                # ok this if statement helps us make new columns when needed.
                if self.implication_count == 10:
                    #reset the count,
                    self.implication_count = 0
                    # then make a new column :)
                    new_column = QtWidgets.QVBoxLayout()
                    self.target_box = new_column
                    self.main_col_5_H.addLayout(self.target_box)
                else:
                    self.implication_count += 1

                new_hori_box = QtWidgets.QHBoxLayout()
                new_hori_box.addWidget(new_label)
                new_hori_box.addWidget(delete_btn)
                self.target_box.addLayout(new_hori_box)

                ## just so you can delete stuff:

                self.delete_btn_label_map[delete_btn] = new_label
                self.delete_button_to_implier_map[delete_btn] = key_tuple
                delete_btn.clicked.connect(self.delete_me)
                self.show()
                # we still need to add stuff in so it actually saves tho
                list_of_consequences_for_saving = tuple(list_of_consequences_for_saving)
                self.implications[key_tuple] = list_of_consequences_for_saving
                self.implications_to_button_map[key_tuple]=new_label


    def delete_me(self):
        self.sender().hide()
        if self.implication_count > 0:
            self.implication_count -= 1
        self.delete_btn_label_map[self.sender()].hide()
        key_tuple = self.delete_button_to_implier_map[self.sender()]
        
        self.implications.pop(key_tuple,None)
    def next_page(self):

        #self.brother.parent.setCurrentWidget(self.brother.parent.page4)
        self.brother.page4.init_ui()
        self.brother.page4.fill_it_all_out()
        self.brother.page4.fill_in_groups()
        self.brother.page4.fill_in_implications()
        self.brother.page4.setWindowTitle("Finalize Everything and Save")
        self.hide()
        #self.brother.page4.show()

class finalize_featureset(QtWidgets.QWidget):
    def __init__(self, brother=None):
        super().__init__()
        self.brother = brother

        #self.attributes = self.brother.current_attributes
        #self.init_ui()
    def init_ui(self):


        # Q frames and titles

        self.features_frame = QFrame()
        self.features_frame.setStyleSheet("background-color: yellow;")
        self.features_frame.setFrameShape(QFrame.StyledPanel)

        self.features_title = QtWidgets.QLabel("Selected Features:")

        self.groups_frame = QFrame()
        self.groups_frame.setStyleSheet("background-color: %s;"%light_teal.name())
        self.groups_frame.setFrameShape(QFrame.StyledPanel)

        self.groups_title = QtWidgets.QLabel("Core Feature-Groups:")

        self.entailments_frame = QFrame()
        self.entailments_frame.setStyleSheet("background-color: %s;"%light_orange.name())
        self.entailments_frame.setFrameShape(QFrame.StyledPanel)

        self.entailments_title = QtWidgets.QLabel("Selected Entailments:")

        self.attributes = self.brother.current_attributes
        self.grandest_hbox = QtWidgets.QHBoxLayout()
        self.features_column = QtWidgets.QVBoxLayout()
        self.features_column_H = QtWidgets.QHBoxLayout(self.features_frame)
        self.features_column.addWidget(self.features_title)
        #self.features_column.addLayout(self.features_column_H)
        self.features_column.addWidget(self.features_frame)
        self.groups_column = QtWidgets.QVBoxLayout(self.groups_frame)

        self.groups_column_mediating_h = QtWidgets.QHBoxLayout()
        self.groups_column_mediating_v = QtWidgets.QVBoxLayout()
        self.groups_column_mediating_v.addWidget(self.groups_title)
        self.groups_column_mediating_v.addWidget(self.groups_frame)


        self.implications_column = QtWidgets.QVBoxLayout()
        self.implications_column_H = QtWidgets.QHBoxLayout(self.entailments_frame)
        #self.implications_column.addLayout(self.implications_column_H)
        self.implications_column.addWidget(self.entailments_title)
        self.implications_column.addWidget(self.entailments_frame)
        #self.implications_column.addStretch(1)

        self.final_column = QtWidgets.QVBoxLayout()

        self.grandest_hbox.addLayout(self.features_column)
        self.grandest_hbox.addLayout(self.groups_column_mediating_v)
        self.grandest_hbox.addLayout(self.implications_column)
        self.grandest_hbox.addLayout(self.final_column)


        #self.fill_it_all_out()
        self.setLayout(self.grandest_hbox)

        # putting in the main buttons
        self.final_column.addStretch(1)
        save_as_label = QtWidgets.QLabel()
        save_as_label.setText("Choose a Name for the Feature Set:")
        save_as_label.setFixedWidth(200)
        self.save_as = QtWidgets.QLineEdit()
        self.save_as.setFixedWidth(200)
        self.final_column.addWidget(save_as_label)
        self.final_column.addWidget(self.save_as)
        save_btn = QtWidgets.QPushButton()
        save_btn.setText("Save")
        save_btn.setFixedWidth(200)
        save_btn.setText("    Confirm and Create")
        save_btn.setIcon(QtGui.QIcon('pictures/save.png'))
        save_btn.setLayoutDirection(QtCore.Qt.RightToLeft)
        save_btn.setIconSize(QtCore.QSize(40, 25))

        save_btn.clicked.connect(self.save_feature_set)
        self.final_column.addWidget(save_btn)
        back_btn = QtWidgets.QPushButton()
        back_btn.setText("Back")
        back_btn.setFixedWidth(200)
        back_btn.setText("             Back")
        back_btn.setIcon(QtGui.QIcon('pictures/Back arrow.png'))
        back_btn.setLayoutDirection(QtCore.Qt.RightToLeft)
        back_btn.setIconSize(QtCore.QSize(40, 25))
        back_btn.clicked.connect(self.back_a_page)
        self.final_column.addWidget(back_btn)
        self.setWindowTitle("Finalize Everything and Save")
    # this fills in the features that are in the thing
    def fill_it_all_out(self):
        # code for resetting the thing here
        # for luku in range (1,self.grand_hbox.count()):
        #     self.grand_hbox.removeItem(self.grand_hbox.itemAt(luku))
        #     
        #

        # self.chosenInventory = self.chooseFeatureSet.currentText()
        # shouldn't need this next line, kuz self.attributes is alrdy defined.
        # self.attributes = [a for a in self.attributes]

        number_of_columns = 2 * (math.ceil(len(self.attributes) / 10))

        column_map = {}
        self.value_map = {}
        self.color_map = {}
        for number in range(number_of_columns):
            new_col = QtWidgets.QVBoxLayout()
            column_map[("column" + str(number))] = new_col

        # tal is swedish for number
        for tal in range(len(self.attributes)):
            col_no = 2 * (math.floor(tal / 10))

            new_label = QtWidgets.QLabel(self.attributes[tal])
            #new_button = QtWidgets.QPushButton("Null")
            #new_pic = QtWidgets.QLabel()
            #new_pic.setPixmap(QtGui.QPixmap("pictures/grey.png"))
            #new_button.clicked.connect(self.alter_value)
            # this line shouldn't be needed
            # new_button.clicked.connect(self.assumption_exec)

            #self.value_map[self.attributes[tal]] = new_button
            #self.color_map[self.attributes[tal]] = new_pic

            #new_lhbox = QtWidgets.QHBoxLayout()
            #new_lhbox.addStretch()
            #new_lhbox.addWidget(new_label)
            #new_lhbox.addStretch()

            #new_hbox = QtWidgets.QHBoxLayout()
            #new_hbox.addStretch()
            #new_hbox.addWidget(new_button)
            #new_hbox.addWidget(new_pic)
            #new_hbox.addStretch()

            #column_map[("column" + str(col_no))].addLayout(new_lhbox)
            #column_map[("column" + str(col_no + 1))].addLayout(new_hbox)
            column_map[("column" + str(col_no))].addWidget(new_label)
        # now to stuff it with filler lines, just so it looks cool :)
        """
        vacuous_lines_needed = len(self.attributes) % 10
        for number in range(vacuous_lines_needed):
            vacuous_label = QtWidgets.QLabel()

            vacuous_hBox = QtWidgets.QHBoxLayout()
            vacuous_hBox.addStretch()
            vacuous_hBox.addWidget(vacuous_label)
            vacuous_hBox.addStretch()

            vacuous_label2 = QtWidgets.QLabel()

            vacuous_lhBox = QtWidgets.QHBoxLayout()
            vacuous_lhBox.addStretch()
            vacuous_lhBox.addWidget(vacuous_label2)
            vacuous_lhBox.addStretch()

            column_map[("column" + str(number_of_columns - 2))].addLayout(vacuous_lhBox)
            column_map[(("column" + str(number_of_columns - 1)))].addLayout(vacuous_hBox)
        """
        for key in column_map:
            self.features_column_H.addLayout(column_map[key])
            column_map[key].addStretch(1)

        # self.setLayout(self.grand_hbox)

        ## this next line will probably need a little changing ; the implication structure should depend on the inventory
        self.implication_structure = {('high1', True): ('low', False), ('low1', True): ('high', False),
                                      ('front1', True): ('back', False), ('back1', True): ('front', False),
                                      ('approximant1', True): ('sonorant', True),
                                      ('syllabic2', True): ('constrG', False), ('sonorant1', True): ('constrG', False),
                                      ('approximant2', True): ('constrG', False), ('voice1', True): ('constrG', False),
                                      ('spreadG1', True): ('constrG', False), ('continuant1', True): ('constrG', False),
                                      ('constrG1', True): ('spreadG', False), ('lateral1', True): ('consonantal', True),
                                      ('delR1', True): ('consonantal', True), ('delR2', True): ('syllabic', False),
                                      ('delR3', True): ('sonorant', False), ('delR4', True): ('approximant', False),
                                      ('delR5', True): ('nasal', False), ('delR6', True): ('round', False),
                                      ('delR7', True): ('atr', None), ('nasal1', True): ('sonorant', True),
                                      ('nasal2', True): ('approximant', False), ('nasal3', True): ('lateral', False),
                                      ('nasal4', True): ('delR', False), ('nasal5', True): ('strident', False),
                                      ('labial', True): ('coronal', False), ('coronal1', True): ('consonantal', True),
                                      ('coronal2', True): ('labial', False), ('coronal3', True): ('round', False),
                                      ('coronal4', False): ('anterior', None), ('anterior1', True): ('coronal', True),
                                      ('anterior2', False): ('coronal', True),
                                      ('distributed', True): ('consonantal', True), ('strident', True): ('delR', True),
                                      ('dorsal1', False): ('high', None), ('dorsal2', False): ('low', None),
                                      ('dorsal3', False): ('front', None), ('dorsal4', False): ('back', None),
                                      ('dorsal5', False): ('atr', None), ('high2', True): ('dorsal', True),
                                      ('low2', True): ('dorsal', True), ('front2', True): ('dorsal', True),
                                      ('back2', True): ('dorsal', True), ('atr1', True): ('dorsal', True),
                                      ('high3', False): ('dorsal', True), ('low3', False): ('dorsal', True),
                                      ('front3', False): ('dorsal', True), ('back3', False): ('dorsal', True),
                                      ('atr2', False): ('dorsal', True), }


        self.setWindowIcon(QtGui.QIcon('pictures/save.png'))
        self.show()
    # this fills in the key natural classes that we made for data organization purposes
    def fill_in_groups(self):
        # you shouldn't have t odo any mumbo jumbo with creating all of these sub columns, and that's becasue
        # you shouldn't permit the user to make more than like 10 groups
        for key in self.brother.feature_groups:
            new_label = QtWidgets.QLabel()
            label_text = ""
            label_text += key
            label_text += " : "
            for tuple in self.brother.feature_groups[key]:
                if tuple[1] == True:
                    label_text += "+ "
                else:
                    label_text += "- "
                label_text += tuple[0]
                label_text += ", "
            new_label.setText(label_text)
            self.groups_column.addWidget(new_label)
            self.show()
        self.groups_column.addStretch(1)
    def fill_in_implications(self):

        
        number_of_columns = len(self.brother.page3.implications)
        number_of_columns = int(number_of_columns/10)
        number_of_columns += 1
        # this just helps us keep track of our columns
        column_list = []
        
        for number in range(number_of_columns):
            
            new_col = QtWidgets.QVBoxLayout()
            column_list.append(new_col)
            self.implications_column_H.addLayout(new_col)
        implication_count = 0
        target_col_no = 0
        
        # ok now just building the string of text we want
        for key in self.brother.page3.implications:
            label_text = ""
            
            for number in range(len(key)):
                if len(key) == 1:
                    if key[number][1] == True:
                        label_text += "+ "
                    elif key[number][1] == False:
                        label_text += "- "
                    elif key[number][1] == None:
                        label_text+= "Null "
                    label_text += key[number][0]
                elif number == len(key)-1:
                    label_text += "and "
                    if key[number][1] == True:
                        label_text += "+ "
                    elif key[number][1] == False:
                        label_text += "- "
                    elif key[number][1] == None:
                        label_text += "Null "
                    label_text += key[number][0]
                elif number == len(key)-2:
                    if key[number][1] == True:
                        label_text += "+ "
                    elif key[number][1] == False:
                        label_text += "- "
                    elif key[number][1] == None:
                        label_text+= "Null "
                    label_text += key[number][0]
                    label_text += " "
                else:
                    if key[number][1] == True:
                        label_text += "+ "
                    elif key[number][1] == False:
                        label_text += "- "
                    elif key[number][1] == None:
                        label_text+= "Null "
                    label_text += key[number][0]
                    label_text += ", "
            
            if len(key) == 1:
                label_text += " implies : "
            else:
                label_text += " imply : "



            for implication in self.brother.page3.implications[key]:
                
                if implication[1] == True:
                    label_text += "+ "
                else:
                    label_text += "- "
                label_text += implication[0]

        # adding the actual label

            new_label = QtWidgets.QLabel()
            new_label.setText(label_text)
            
            
            column_list[target_col_no].addWidget(new_label)

        # now just handling which column it will be added on to in the future

            implication_count += 1

            if implication_count > 9:
                
                implication_count = 0
                target_col_no += 1
        # now just to make it look prettier, so that things get added from top to bottom, not bottom to top or whatever

        for column in column_list:
            column.addStretch(1)
    def back_a_page(self):
        #self.brother.parent.setCurrentWidget(self.brother.parent.page3)
        reset4 = finalize_featureset(self.brother)
        self.brother.page4 = reset4
        #self.brother.parent.addWidget(self.brother.parent.page4)
        self.hide()
        self.brother.page3.show()
        self.brother = None
    def save_feature_set(self):
        name = self.save_as.text()
        if name == "":
            hey_man_icon_giver = QMainWindow()
            hey_man_icon_giver.setWindowIcon(QtGui.QIcon("pictures/aviso"))
            hey_man_icon_giver.hide()
            hey_man = QtWidgets.QMessageBox.information(hey_man_icon_giver, "Choose Name",
                                                    "You Must First Select a Name for your Feature Set",
                                                    QMessageBox.Ok)
            hey_man_icon_giver.close()
        else:
            attributes = [a for a in self.attributes]
            new_class = class_creator(name,attributes)
            # this list of tuples is what will get saved for later. then we can have the machine just dynamically
            # create all the classes at startup.
            #class_tuples.append((name,attributes))
            feature_set_map[name]=attributes
            set_map[name] = {"All Phonemes":[]}
            dictionish[name] =[]
            inventories[name]= {'All Phonemes':[]}
            technical_map[name] = {}
            # I'm sorry, the directories for where these bits of data are stored are just poorly designed. It's kind
            # of hard to follow, that's my bad.
            technical_map[name]["keyCategories"] = self.brother.feature_groups
            technical_map[name]["Entailments"] = self.brother.page3.implications

            
            inventory_update.set_off()

            
            self.brother.parent.executive_window.chooseInventory.addItem(name)
            hey_man = QtWidgets.QMessageBox.information(self, "Success",
                                                        "New Featureset Created Successully. Be sure to save your data afterwards if you are sure that you want to keep it.",
                                                        QMessageBox.Ok)



            self.brother.close()
            self.close()

class edit_featureset_opening_page(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon('pictures/Edit.png'))


        self.layout = QtWidgets.QVBoxLayout()
        self.logo = QtGui.QPixmap('pictures/Edit.png')
        self.logo = self.logo.scaled(250, 150, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.picture = QtWidgets.QLabel()
        self.picture.setPixmap(self.logo)
        self.picture.setFixedWidth(250)
        self.layout.addWidget(self.picture)

        self.prompt = QtWidgets.QLabel("Choose Which Featureset to Edit")
        self.layout.addWidget(self.prompt)
        self.choose_box = QtWidgets.QComboBox()
        self.choose_box.addItem("Null")
        self.setWindowTitle("Edit Featureset")
        for key in feature_set_map:
            self.choose_box.addItem(key)
        self.layout.addWidget(self.choose_box)
        self.choice_box = QtWidgets.QHBoxLayout()
        self.features_btn = QtWidgets.QPushButton("Edit Features")
        self.feature_groups_btn = QtWidgets.QPushButton("Edit Feature-Groups")
        self.entailments_btn = QtWidgets.QPushButton("Edit Entailments")
        self.choice_box.addWidget(self.features_btn)
        self.choice_box.addWidget(self.feature_groups_btn)
        self.choice_box.addWidget(self.entailments_btn)
        self.layout.addLayout(self.choice_box)
        self.setLayout(self.layout)
        self.setWindowTitle("Edit A Featureset")
        self.show()

        self.feature_edit_page = edit_featureset(self)
        self.feature_group_edit_page = edit_feature_groups(self)
        self.edit_entailments= edit_implications(self)

        self.features_btn.clicked.connect(self.show_feature_edit)
        self.feature_groups_btn.clicked.connect(self.show_feature_group_edit)
        self.entailments_btn.clicked.connect(self.show_entailment_edit)

    def show_feature_edit(self):
        if self.choose_box.currentText() == "Null":
            hey_man = QtWidgets.QMessageBox.warning(self, "Feature Set not Chosen",
                                                    "You Must First Select a Feature Set",
                                                    QMessageBox.Ok)
        else:
            self.feature_edit_page = edit_featureset(self)
            self.feature_edit_page.init_ui()
            #self.feature_edit_page.show()
            #if self.feature_edit_page.loaded != True:
            #    self.feature_edit_page.init_ui()
            #    self.feature_edit_page.loaded = True

    def show_feature_group_edit(self):
        if self.choose_box.currentText() == "Null":
            hey_man = QtWidgets.QMessageBox.warning(self, "Feature Set not Chosen",
                                                    "You Must First Select a Feature Set",
                                                    QMessageBox.Ok)
        else:
            self.feature_group_edit_page = edit_feature_groups(self)
            self.feature_group_edit_page.init_ui()
            #self.feature_group_edit_page.show()
            #if self.feature_group_edit_page.loaded == False:
            #    self.feature_group_edit_page.chosenInventory = self.choose_box.currentText()
            #    self.feature_group_edit_page.init_ui()
            #    self.feature_group_edit_page.loaded = True
    def show_entailment_edit(self):
        if self.choose_box.currentText() == "Null":
            hey_man = QtWidgets.QMessageBox.warning(self, "Feature Set not Chosen",
                                                    "You Must First Select a Feature Set",
                                                    QMessageBox.Ok)
        else:
            self.edit_entailments = edit_implications(self)
            self.edit_entailments.init_ui()

            #self.edit_entailments.show()
            #if self.edit_entailments.loaded == False:
            #    self.edit_entailments.chosenInventory = self.choose_box.currentText()
            #    self.edit_entailments.init_ui()
            #    self.edit_entailments.loaded = True

class edit_featureset(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.loaded = False
        self.setWindowTitle("Edit Features")
        self.setWindowIcon(QtGui.QIcon('pictures/Edit.png'))
    def init_ui(self):


        ## Q Frames

        self.left_frame = QtWidgets.QFrame()
        self.left_frame.setStyleSheet("background-color: %s;"%light_teal.name())
        self.left_frame.setFrameShape(QFrame.StyledPanel)

        self.right_frame = QtWidgets.QFrame()
        self.right_frame.setStyleSheet("background-color: %s;"%light_orange.name())

        self.right_frame.setFrameShape(QFrame.StyledPanel)

        ### other pages
        self.page2 = make_feature_groups(self)
        self.page3 = make_implications(self)
        self.page4 = finalize_featureset(self)

        ## for saving
        self.feature_groups = {}


        ## top stuff -- I think I've goofed here.
        self.top_box = QtWidgets.QHBoxLayout()
        self.top_box_left = QtWidgets.QVBoxLayout()
        self.top_box_right = QtWidgets.QVBoxLayout()

        self.added_features_label = QtWidgets.QLabel("Added Features")
        self.add_and_import_label = QtWidgets.QLabel("Add and Import Features")
        self.top_box_right.addWidget(self.added_features_label)


        # left column stuff




        self.save_as_label = QtWidgets.QLabel("Choose a Name")
        self.save_as_line = QtWidgets.QLineEdit()
        self.save_btn = QtWidgets.QPushButton("Save Changes")
        self.save_btn.setIcon(QtGui.QIcon('pictures/save.png'))
        self.add_feature_label = QtWidgets.QPushButton("Add a Feature")
        self.add_feature_label.setStyleSheet("background-color: %s;"%light_gray.name())
        self.add_feature_as = QtWidgets.QLineEdit()
        self.add_feature_as.setStyleSheet("background-color: white;")

        #self.window_size = 0

        self.leftColumn = QtWidgets.QVBoxLayout(self.left_frame)


        #self.leftColumn.addWidget(self.save_as_label)
        #self.leftColumn.addWidget(self.save_as_line)
        self.leftColumn.addStretch(1)
        self.leftColumn.addWidget(self.add_feature_label)
        self.leftColumn.addWidget(self.add_feature_as)
        self.leftColumn.addWidget(self.save_btn)
        self.leftColumn.addStretch(1)
        # this little bit of gymnastics allows me to set the width of the column that the vBox is.

        #self.Vwidth_widget = QtWidgets.QWidget()
        #self.Vwidth_widget.setLayout(self.leftColumn)
        #self.Vwidth_widget.setFixedWidth(200)
        subVbox = QtWidgets.QVBoxLayout()
        subVbox.addStretch(1)
        #subVbox.addWidget(self.Vwidth_widget)
        subVbox.addWidget(self.left_frame)
        subVbox.addStretch(1)

        # right column stuff

        self.rightColumnOuter = QtWidgets.QHBoxLayout(self.right_frame)
        self.rightColumnInner = QtWidgets.QVBoxLayout()

        self.widgetCount = 0
        self.appendable_column = self.rightColumnInner
        self.buttonColumnMap ={}

        rightColumn = QtWidgets.QVBoxLayout()
        rightColumn.addStretch(1)

        self.features_added_so_far = QtWidgets.QLabel("Features Added so Far:")
        rightColumn.addWidget(self.features_added_so_far)
        self.rightColumnOuter.addLayout(self.rightColumnInner)
        rightColumn.addWidget(self.right_frame)
        rightColumn.addStretch(1)

        grandBox = QtWidgets.QHBoxLayout()

        grandBox.addLayout(subVbox)
        grandBox.addLayout(rightColumn)

        ## Feature set selection
        self.inventories = [a for a in feature_set_map]
        self.chosenInventory = self.parent.choose_box.currentText()

        # this keeps track of how many attributes are out there, so when we got to save we know what to save
        self.current_attributes = []


        self.add_feature_label.clicked.connect(self.add_feature)
        self.save_btn.clicked.connect(self.save_changes)
        self.setLayout(grandBox)
        self.setWindowTitle("Select Features")

        self.import_features()
        self.setMinimumWidth(812)
        self.show()


        # keepin track of stuff

    def add_feature(self):
        if self.add_feature_as.text() == "":
            pass
        else:
            text = self.add_feature_as.text()
            ## normalizing the input, trimming off any excess spaces
            text = text.lower()
            trim = True
            while trim:
                trim = False
                if text[len(text)-1] == ' ':
                    text = text[0:len(text)-1]
                    trim = True

            if text in self.current_attributes:
                
                hey_man = QtWidgets.QMessageBox.warning(self,"Feature Already Present","You've already added this feature. No redundancy allowed.",QMessageBox.Ok)
            else:
                
                new_button = QtWidgets.QPushButton(text)
                new_button.setFixedWidth(100)
                new_button.setToolTip("Click to Delete")

                ## if the number gets to big, we should change columns
                if self.widgetCount == 7:
                    self.widgetCount =0
                    self.new_layout = QtWidgets.QVBoxLayout()
                    self.rightColumnOuter.addLayout(self.new_layout)
                    self.appendable_column = self.new_layout

                self.current_attributes.append(text)
                new_button.setStyleSheet("background-color: %s;"%light_gray.name())
                self.appendable_column.addWidget(new_button)
                self.buttonColumnMap[new_button] = self.appendable_column
                new_button.clicked.connect(partial(self.remove_feature,new_button))

                ## you need to at clicking functionality here

                self.show()


                self.widgetCount += 1
    def remove_feature(self,button):
        
        self.current_attributes = [a for a in self.current_attributes if a != button.text()]
        button.hide()
        self.buttonColumnMap[button].removeWidget(button)
        self.show()

    def import_features(self):
        # I think I defined an .attributes function
        

        
        
        
        #self.attributes = [a for a in set_map[self.chosenInventory]["All Phonemes"][0].attributes]
        self.attributes = [a for a in feature_set_map[self.chosenInventory] if a != "Name"]
        
        self.attributes = [a for a in self.attributes if a != "name"]

        for attribute in self.attributes:
            self.add_feature_as.setText(attribute)
            self.add_feature()
            self.add_feature_as.setText('')
    ### This next method prolly shouldn't be here
    def save_changes(self):
        hey_man = QtWidgets.QMessageBox.question(self, 'Saving Changes',
                                                 'Are You Sure You Want to Change the %s Featureset?'%(self.chosenInventory),
                                                 QMessageBox.Yes | QMessageBox.No)
        if hey_man == QMessageBox.Yes:
            
            current_attributes = self.current_attributes
            old_attributes = feature_set_map[self.chosenInventory]
            
            new_attributes = [a for a in current_attributes if a not in old_attributes]
            
            feature_set_map[self.chosenInventory] = current_attributes
            
            deleted_attributes = [a for a in old_attributes if a not in current_attributes]
            ### resetting dictionish
            new_dictionish_entry = []
            for phoneme_tuple in dictionish[self.chosenInventory]:
                new_phoneme_tuple =[]
                # salvaging the old ones
                for attribute in phoneme_tuple:
                    if attribute[0] in current_attributes or attribute[0] == "name":
                        new_phoneme_tuple.append(attribute)
                # adding in blanks for the new one
                for attribute in new_attributes:
                    new_phoneme_tuple.append((attribute,None))
                new_phoneme_tuple = tuple(new_phoneme_tuple)
                new_dictionish_entry.append(new_phoneme_tuple)

            dictionish[self.chosenInventory] = new_dictionish_entry
            inventory_update.set_off()
            reset_phoneme_map()


            
            

            ### Now we need to reset the the stuff in the technical map. If there are any Key Categories tha reference
            ### any deleted features, or that have any entailment relationships, we gotta get rid of those.

            ### iterate through each keyCategory of the affected featureset
            delete_me = []
            for group in technical_map[self.chosenInventory]["keyCategories"]:
                ### iterate through each keyCategory - did it have a now-deleted attribute?
                ### if it does, you gotta rebuild the definition, and add it back in - unless the category is now empty
                
                new_definition = []
                redefinition_necessary = False
                
                
                for defining_characteristic in technical_map[self.chosenInventory]["keyCategories"][group]:
                    
                    
                    if defining_characteristic[0] in deleted_attributes:
                        
                        redefinition_necessary = True
                    else:
                        new_definition.append(defining_characteristic)

                if redefinition_necessary == True and len(new_definition)>0:
                    new_definition = tuple(new_definition)
                    technical_map[self.chosenInventory]["keyCategories"][group] = new_definition
                elif redefinition_necessary == True and len(new_definition) == 0:
                    
                    delete_me.append(group)
                    
                else:
                    pass

            for deleteable in delete_me:
                technical_map[self.chosenInventory]["keyCategories"].pop(deleteable,None)


            
            ### ok good, nowe we gotta just make sure none of the entailments are goofy. You gotta do the same thing, basically
            delete_me =[]
            for entailment in technical_map[self.chosenInventory]["Entailments"]:
                new_entailment = []
                new_entailment_necessary = False

                if entailment[0] in deleted_attributes:
                    technical_map[self.chosenInventory]["Entailments"].pop(entailment,None)
                else:
                    for entailed in technical_map[self.chosenInventory]["Entailments"][entailment]:
                        if entailed[0] in deleted_attributes:
                            new_entailment_necessary = True
                        else:
                            new_entailment.append(entailed)

                    if new_entailment_necessary == True and len(new_entailment) > 0:
                        new_entailment = tuple(new_entailment)
                        technical_map[self.chosenInventory]["Entailments"][entailment] = new_entailment
                    elif  new_entailment_necessary == True and len(new_entailment) == 0:
                        delete_me.append(entailment)
                    else:
                        pass


            for deleteable in delete_me:
                technical_map[self.chosenInventory]["Entailments"].pop(deleteable,None)
            
            


            self.close()
        else:
            pass

class edit_feature_groups(QtWidgets.QWidget):
    def __init__(self,Parent=None):
        super().__init__()
        self.parent = Parent
        self.chosenInventory = "Null"
        self.loaded = False
        self.feature_groups = {}
        self.setWindowTitle("Edit Feature Groups")
        self.setWindowIcon(QtGui.QIcon('pictures/Edit.png'))
        # self.attributes = self.brother.current_attributes
        # self.init_ui()
    def init_ui(self):
        # migh need to do more here
        # do you need to do fill it all out when inintializing?

        ## Q Frames

        self.button_frame = QtWidgets.QFrame()
        self.button_frame.setStyleSheet("background-color: %s;"%light_yellow.name())
        self.button_frame.setFrameShape(QFrame.StyledPanel)

        self.groups_frame = QtWidgets.QFrame()
        self.groups_frame.setStyleSheet("background-color: %s;"%light_orange.name())
        self.groups_frame.setFrameShape(QFrame.StyledPanel)

        self.chosenInventory = self.parent.choose_box.currentText()
        self.feature_groups = {}
        for key in technical_map[self.chosenInventory]["keyCategories"]:
            self.feature_groups[key] = technical_map[self.chosenInventory]["keyCategories"][key]
        self.attributes = []

        self.value_map = {}
        self.color_map = {}
        self.grander_hbox = QtWidgets.QHBoxLayout()
        self.grander_hbox.addStretch()
        self.grand_hbox = QtWidgets.QHBoxLayout()
        self.grand_hbox.addStretch()

        self.right_side = QtWidgets.QVBoxLayout(self.button_frame)
        self.save_label = QtWidgets.QLabel("Choose a Name for the Group")
        self.save_btn = QtWidgets.QPushButton("Add Group")
        self.save_btn.setStyleSheet("background-color: white;")
        self.save_btn.setIcon(QtGui.QIcon('pictures/plus sign.png'))

        self.save_btn.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.save_btn.setIconSize(QtCore.QSize(40, 25))


        self.done_btn = QtWidgets.QPushButton("Save Changes")
        self.done_btn.setStyleSheet("background-color: %s;"%light_teal.name())
        self.done_btn.setIcon(QtGui.QIcon('pictures/save.png'))
        self.done_btn.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.done_btn.setIconSize(QtCore.QSize(40, 25))

        self.save_btn.setFixedWidth(200)
        self.save_btn.setFixedHeight(50)
        self.done_btn.setFixedWidth(200)
        self.done_btn.setFixedHeight(30)
        self.save_as = QtWidgets.QLineEdit()
        self.save_as.setStyleSheet("background-color: white;")
        self.save_as.setFixedWidth(200)
        self.right_side.addWidget(self.save_label)
        self.right_side.addWidget(self.save_as)
        self.right_side.addWidget(self.save_btn)
        self.right_side.addWidget(self.done_btn)

        self.righter_side = QtWidgets.QHBoxLayout(self.groups_frame)
        self.righter_side_column = QtWidgets.QVBoxLayout()
        #some gymnastics to make sure the features are added from top to bottom, not bottom to top.
        self.righter_side_column_2 = QtWidgets.QVBoxLayout()
        self.righter_side_column_2.addLayout(self.righter_side_column)
        self.righter_side_column_2.addStretch(1)

        self.righter_side.addLayout(self.righter_side_column_2)
        self.groups_header = QtWidgets.QLabel()
        self.groups_header.setText("Natural Classes Made So Far")
        #self.righter_side_column.addWidget(self.groups_header)
        self.righter_side_column.addStretch(0)

        ## to make the Qframe work
        self.righter_side_2 = QtWidgets.QVBoxLayout()
        self.righter_side_2.addWidget(self.groups_header)
        self.righter_side_2.addWidget(self.groups_frame)

        self.grander_hbox.addLayout(self.grand_hbox)

        #self.grander_hbox.addLayout(self.right_side)

        ## this to make the button frame not span the whole thing
        self.right_side_2 = QtWidgets.QVBoxLayout()
        self.vacuous_label = QtWidgets.QLabel()
        self.right_side_2.addWidget(self.vacuous_label)
        self.right_side_2.addWidget(self.button_frame)
        self.right_side_2.addStretch(1)
        self.grander_hbox.addLayout(self.right_side_2)
        #self.grander_hbox.addLayout(self.righter_side)
        self.grander_hbox.addLayout(self.righter_side_2)
        self.setLayout(self.grander_hbox)

        self.show()
        self.save_btn.clicked.connect(self.add_group)
        self.done_btn.clicked.connect(self.save_it_all)
        # so that you can delete stuff
        self.button_label_map = {}
        self.button_box_map = {}
        self.button_name_map = {}

        self.group_count = 0
        self.setWindowTitle("Edit the Primary Feature-Groups")
        self.fill_it_all_out()
        self.show_what_youve_done_so_far()

    def fill_it_all_out(self, ):
        # code for resetting the thing here
        # for luku in range (1,self.grand_hbox.count()):
        #     self.grand_hbox.removeItem(self.grand_hbox.itemAt(luku))
        #     
        #

        # self.chosenInventory = self.chooseFeatureSet.currentText()
        # shouldn't need this next line, kuz self.attributes is alrdy defined.
        # self.attributes = [a for a in self.attributes]

        self.attributes = feature_set_map[self.chosenInventory]

        number_of_columns = 2 * (math.ceil(len(self.attributes) / 10))

        column_map = {}
        self.value_map = {}
        self.color_map = {}
        for number in range(number_of_columns):
            new_col = QtWidgets.QVBoxLayout()
            column_map[("column" + str(number))] = new_col

        # tal is swedish for number
        for tal in range(len(self.attributes)):
            col_no = 2 * (math.floor(tal / 10))

            new_label = QtWidgets.QLabel(self.attributes[tal] + ":")
            new_button = QtWidgets.QPushButton("Null")
            new_pic = QtWidgets.QLabel()
            new_pic.setPixmap(QtGui.QPixmap("pictures/grey.png"))
            new_button.clicked.connect(self.alter_value)
            # this line shouldn't be needed
            # new_button.clicked.connect(self.assumption_exec)

            self.value_map[self.attributes[tal]] = new_button
            self.color_map[self.attributes[tal]] = new_pic

            # I'm changing this
            #new_lhbox = QtWidgets.QHBoxLayout()
            #new_lhbox.addStretch()
            #new_lhbox.addWidget(new_label)
            #new_lhbox.addStretch()

            new_hbox = QtWidgets.QHBoxLayout()
            #new_hbox.addStretch(1)
            new_hbox.addWidget(new_label)
            new_hbox.addStretch(1)
            new_hbox.addWidget(new_button)
            new_hbox.addWidget(new_pic)
            #new_hbox.addStretch(1)

            #column_map[("column" + str(col_no))].addLayout(new_lhbox)
            column_map[("column" + str(col_no + 1))].addLayout(new_hbox)

        # now to stuff it with filler lines, just so it looks cool :)
        """
        vacuous_lines_needed = len(self.attributes) % 10
        for number in range(vacuous_lines_needed):
            vacuous_label = QtWidgets.QLabel()

            vacuous_hBox = QtWidgets.QHBoxLayout()
            vacuous_hBox.addStretch()
            vacuous_hBox.addWidget(vacuous_label)
            vacuous_hBox.addStretch()

            vacuous_label2 = QtWidgets.QLabel()

            vacuous_lhBox = QtWidgets.QHBoxLayout()
            vacuous_lhBox.addStretch()
            vacuous_lhBox.addWidget(vacuous_label2)
            vacuous_lhBox.addStretch()

            column_map[("column" + str(number_of_columns - 2))].addLayout(vacuous_lhBox)
            column_map[(("column" + str(number_of_columns - 1)))].addLayout(vacuous_hBox)
        """

        for key in column_map:
            self.grand_hbox.addLayout(column_map[key])
            column_map[key].addStretch(1)
        # self.setLayout(self.grand_hbox)



        self.show()

    def show_what_youve_done_so_far(self):
        for keyCategory in technical_map[self.chosenInventory]["keyCategories"]:

            label_text = keyCategory
            label_text += " :"
            for tuple in technical_map[self.chosenInventory]["keyCategories"][keyCategory]:
                if tuple[1] == True:
                    label_text += " + "
                else:
                    label_text += " - "
                label_text += tuple[0]
                label_text += ","

            new_horiz_box = QtWidgets.QHBoxLayout()
            new_label = QtWidgets.QLabel()
            new_label.setText(label_text)
            new_label.setWordWrap(True)
            new_label.setFixedWidth(100)
            delete_button = QtWidgets.QPushButton()
            delete_button.setText("Delete")
            delete_button.setFixedWidth(75)
            new_horiz_box.addWidget(new_label)
            new_horiz_box.addWidget(delete_button)

            delete_button.setStyleSheet("background-color: %s;"%light_gray.name())
            self.righter_side_column.addLayout(new_horiz_box)

            # now making the button removable
            delete_button.clicked.connect(partial(self.remove_group, delete_button))
            self.button_label_map[delete_button] = new_label
            self.button_box_map[delete_button] = new_horiz_box

            # now we gotta save the group
            self.button_name_map[delete_button] = keyCategory
            self.group_count += 1

    def alter_value(self):
        sender = self.sender()
        for key in self.value_map:
            if self.value_map[key] == sender:
                color_label = self.color_map[key]
        if sender.text() == 'Null':
            sender.setText('True')
            color_label.setPixmap(QtGui.QPixmap('pictures/green.png'))
        elif sender.text() == 'True':
            sender.setText('False')
            color_label.setPixmap(QtGui.QPixmap('pictures/red.png'))
        elif sender.text() == 'False':
            sender.setText('Null')
            color_label.setPixmap(QtGui.QPixmap('pictures/grey.png'))

    def add_group(self):
        ## normalizing the input, trimming off any excess spaces
        
        group_name = self.save_as.text()
        if group_name == "":
            hey_man = QtWidgets.QMessageBox.warning(self, "Name Required!", "You Need to Enter a Name for Your Group First!",
                                                    QMessageBox.Ok)
        else:
            group_name = group_name.lower()
            trim = True
            while trim:
                trim = False
                if group_name[len(group_name) - 1] == ' ':
                    group_name = group_name[0:len(group_name) - 1]
                    trim = True
            if group_name == "":
                hey_man = QtWidgets.QMessageBox.warning(self, "Name Required!",
                                                        "You Need to Enter a Name for Your Group First!", QMessageBox.Ok)
            elif self.group_count > 8:
                hey_man = QtWidgets.QMessageBox.warning(self, "Too Many Groups",
                                                        "You've Made Too Many Groups.",
                                                        QMessageBox.Ok)
            else:
                
                # making the tuple so that it can be compared
                group_name = group_name[0].upper() + group_name[1:len(group_name)]
                list_of_defining_attributes = []
                label_text = ""
                label_text += group_name
                label_text += ": "
                for key in self.value_map:
                    if self.value_map[key].text() == 'True':
                        label_text += (" + " + key)
                        new_tuple = (key, True)
                        list_of_defining_attributes.append(new_tuple)
                    elif self.value_map[key].text() == 'False':
                        label_text += (" - " + key)
                        new_tuple = (key, False)
                        list_of_defining_attributes.append(new_tuple)

                end_tuple = tuple(list_of_defining_attributes)
                # another wave of conditions
                redundant_class = False
                
                
                for group in self.feature_groups:
                    if self.is_the_group_the_same(self.feature_groups[group], end_tuple) == True:
                        redundant_class = True
                if group_name in self.feature_groups:
                    hey_man = QtWidgets.QMessageBox.warning(self, "The name is taken",
                                                            "You May Not Have Two Groups With One Name",
                                                            QMessageBox.Ok)
                elif redundant_class == True:
                    hey_man = QtWidgets.QMessageBox.warning(self, "Redundant Group",
                                                            "You Already Have a Group With the Same Features",
                                                            QMessageBox.Ok)
                elif len(list_of_defining_attributes) == 0:
                    hey_man = QtWidgets.QMessageBox.warning(self, "No Defining Features",
                                                            "Pick Some Features to Define the Group First.",
                                                            QMessageBox.Ok)
                else:
                    
                    new_horiz_box = QtWidgets.QHBoxLayout()
                    new_label = QtWidgets.QLabel()
                    new_label.setText(label_text)
                    new_label.setWordWrap(True)
                    new_label.setFixedWidth(100)
                    delete_button = QtWidgets.QPushButton()
                    delete_button.setText("Delete")
                    delete_button.setFixedWidth(75)
                    delete_button.setStyleSheet("background-color: %s;"%light_gray.name())
                    new_horiz_box.addWidget(new_label)
                    new_horiz_box.addWidget(delete_button)
                    self.righter_side_column.addLayout(new_horiz_box)
                    
                    # now making the button removable
                    delete_button.clicked.connect(partial(self.remove_group, delete_button))
                    self.button_label_map[delete_button] = new_label
                    self.button_box_map[delete_button] = new_horiz_box
                    
                    # now we gotta save the group
                    
                    self.feature_groups[group_name] = end_tuple
                    
                    self.button_name_map[delete_button] = group_name
                    self.group_count += 1
                    
    def remove_group(self, button):
        button.hide()
        group_name = self.button_label_map[button]
        self.button_label_map[button].hide()
        ## ?? why do I not need this line? I'm confused. It works well without it, but you'd think that you'd need
        ## to remove the label AND the button. /shrug
        # self.button_box_map[button].removeWidget(button_label_map[button])

        self.button_box_map[button].removeWidget(button)
        self.show()
        self.group_count -= 1

        # now to actually remove the data
        self.feature_groups.pop(self.button_name_map[button], None)



    def is_the_group_the_same(self, tuple_of_tuples_1, tuple_of_tuples_2):
        are_they_the_same = True
        testing_dictionary_1 = {}
        testing_dictionary_1_len = 0
        for tuple in tuple_of_tuples_1:
            testing_dictionary_1[tuple[0]] = tuple[1]
            testing_dictionary_1_len += 1
        testing_dictionary_2 = {}
        testing_dictionary_2_len = 0
        for tuple in tuple_of_tuples_2:
            testing_dictionary_2[tuple[0]] = tuple[1]
            testing_dictionary_2_len += 1
        for key in testing_dictionary_1:
            if key not in testing_dictionary_2:
                are_they_the_same = False
            elif testing_dictionary_1[key] != testing_dictionary_2[key]:
                are_they_the_same = False
            elif testing_dictionary_1_len != testing_dictionary_2_len:
                are_they_the_same = False
            else:
                pass
        return (are_they_the_same)


    def save_it_all(self):
        hey_man = QMessageBox.question(self,"Are you sure?","Are you sure that you want to save changes to the "
                                                            "feature groups?",QMessageBox.Yes|QMessageBox.No)
        if hey_man == QMessageBox.No:
            pass
        else:
            
            
            ## this bottom line is how the featuregroups SHOULD be getting saved, but there is another mechanism that's doing it and I don't know what.
            technical_map[self.chosenInventory]["keyCategories"] = self.feature_groups

            

            inventory_update.set_off()
            self.close()
            self.parent.close()

class edit_implications(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.chosenInventory = "Null"
        self.loaded = False
        self.setWindowTitle("Edit Entailments")
        self.setWindowIcon(QtGui.QIcon('pictures/Edit.png'))
    def init_ui(self):
        # migh need to do more here
        # do you need to do fill it all out when inintializing?

        self.move(215, 279)

        self.setFixedHeight(350)

        self.chosenInventory = self.parent.choose_box.currentText()

        # Frames for key columns 4 and 5, which correspond to the add buttons and also the entailments made thus far
        self.col_4_frame = QtWidgets.QFrame()
        self.col_4_frame.setStyleSheet("background-color: %s;"%light_yellow.name())
        self.col_4_frame.setFrameShape(QFrame.StyledPanel)

        self.col_5_frame = QtWidgets.QFrame()
        self.col_5_frame.setStyleSheet("background-color: %s;"%light_orange.name())
        self.col_5_frame.setFrameShape(QFrame.StyledPanel)

        self.value_map = {}
        self.color_map = {}
        self.implier_value_map = {}
        self.implier_color_map = {}
        self.grandest_hbox = QtWidgets.QHBoxLayout()
        self.main_col_1 = QtWidgets.QVBoxLayout()
        self.main_col_1_H = QtWidgets.QHBoxLayout()
        self.main_col_2 = QtWidgets.QVBoxLayout()
        self.main_col_3 = QtWidgets.QVBoxLayout()
        self.main_col_3_H = QtWidgets.QHBoxLayout()
        self.main_col_4 = QtWidgets.QVBoxLayout(self.col_4_frame)




        self.main_col_1.addLayout(self.main_col_1_H)
        self.main_col_3.addLayout(self.main_col_3_H)


        self.grandest_hbox.addLayout(self.main_col_1)
        self.grandest_hbox.addLayout(self.main_col_2)
        self.grandest_hbox.addLayout(self.main_col_3)
        #self.grandest_hbox.addLayout(self.main_col_4)
        #self.grandest_hbox.addLayout(self.main_col_5)

        # to make sure the frame doesn't stretch the whole way, but rather is only under the buttons.
        self.main_col_4_2 = QtWidgets.QVBoxLayout()
        self.main_col_4_2.addStretch(1)
        self.main_col_4_2.addWidget(self.col_4_frame)
        self.main_col_4_2.addStretch(1)

        self.grandest_hbox.addLayout(self.main_col_4_2)

        # The fifth column is a little confusing. You have col_5_2 on the outisde, within which you have
        # the label and then another column, 5_3. Col 5_3 has the frame as it's parent and also has the stretch
        # so that the frame goes all the way to the bottom. Within col 5_3 is another column, col 5_4, which has a stretch
        # added to it to make sure that the
        # entailments are added from top to bottom, not botom to top. Then, within that one is main _col 5 H, which is a horizontal
        # column that will house all the vertical columns (such as maincol_5_V and the dynamically generated ones)
        # that end up housing the  entailments themselves.

        self.main_col_5_H = QtWidgets.QHBoxLayout()
        self.maincol_5_V = QtWidgets.QVBoxLayout()
        self.stretchie = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.maincol_5_V.addItem(self.stretchie)
        self.col_5_2 = QtWidgets.QVBoxLayout()
        self.entailments_here_label = QtWidgets.QLabel("Entailments added so far:")
        self.col_5_2.addWidget(self.entailments_here_label)
        self.col_5_3 = QtWidgets.QVBoxLayout(self.col_5_frame)
        self.col_5_2.addWidget(self.col_5_frame)


        self.col_5_4 = QtWidgets.QVBoxLayout()

        self.col_5_3.addLayout(self.col_5_4)
        self.col_5_4.addLayout(self.main_col_5_H)
        #self.col_5_4.addStretch(1)

        self.main_col_5_H.addLayout(self.maincol_5_V)

        self.grandest_hbox.addLayout(self.col_5_2)

        self.implication_extra1 = QtWidgets.QLabel()
        self.implication_extra1.setPixmap(QtGui.QPixmap('pictures/other implies arrow.png'))
        self.implication_extra2 = QtWidgets.QLabel()
        self.implication_extra2.setPixmap(QtGui.QPixmap('pictures/other implies arrow.png'))

        self.implication_arrow = QtWidgets.QLabel()
        self.implication_arrow.setPixmap(QtGui.QPixmap('pictures/Impliesarrow.png'))

        self.main_col_2.addWidget(self.implication_extra1)
        self.main_col_2.addWidget(self.implication_arrow)
        self.main_col_2.addWidget(self.implication_extra2)
        self.main_col_2.addStretch(1)

        self.add_button = QtWidgets.QPushButton()
        self.add_button.setText("Add Implication")
        self.add_button.clicked.connect(self.add_implication)
        self.add_button.setFixedHeight(50)
        self.add_button.setFixedWidth(200)

        self.add_button.setIcon(QtGui.QIcon('pictures/plus sign.png'))
        # self.save_btn.setText("            Next")
        self.add_button.setLayoutDirection(QtCore.Qt.RightToLeft)
        # self.save_btn.setFixedHeight(30)
        self.add_button.setIconSize(QtCore.QSize(40, 25))

        self.save_btn = QtWidgets.QPushButton()
        self.save_btn.setText("Save Featureset")
        self.save_btn.clicked.connect(self.save_it_all)

        self.save_btn.setIcon(QtGui.QIcon('pictures/save.png'))
        # self.save_btn.setText("            Next")
        self.save_btn.setLayoutDirection(QtCore.Qt.RightToLeft)
        # self.save_btn.setFixedHeight(30)
        self.save_btn.setIconSize(QtCore.QSize(40, 25))

        self.save_btn.setFixedHeight(50)
        self.save_btn.setFixedWidth(200)




        self.main_col_4.addWidget(self.add_button)
        self.main_col_4.addWidget(self.save_btn)
        # tooltips
        self.add_button.setToolTip("Click here to add an entailment")




        # implicationcount allows you to make sure that when you add too many implications, they will
        # form new columns instead of just making one big fat long column.

        self.implication_count = 1
        self.target_box = self.maincol_5_V


        # so you can delete implications:
        self.delete_btn_label_map = {}


        #self.target_box.addWidget(self.entailments_here_label)
        #self.target_box.addStretch(0)


        # so that you can delete stuff
        self.button_label_map = {}
        self.button_box_map = {}
        self.delete_button_to_implier_map = {}

        # Lastly, to save the data.
        self.implications = {}

        self.implications_to_button_map = {}
        self.setWindowTitle("Set Entailments for the Featureset")

        self.attributes = feature_set_map[self.chosenInventory]
        self.implication_count = 0
        self.fill_it_all_out(self.main_col_1_H, True)
        self.fill_it_all_out(self.main_col_3_H, False)
        self.show_what_we_already_got()
        self.setLayout(self.grandest_hbox)

    def fill_it_all_out(self,recipient_box,implier = None):

        # this function puts the buttons where want them.

        # code for resetting the thing here
        # for luku in range (1,self.grand_hbox.count()):
        #     self.grand_hbox.removeItem(self.grand_hbox.itemAt(luku))
        #     
        #

        # self.chosenInventory = self.chooseFeatureSet.currentText()
        # shouldn't need this next line, kuz self.attributes is alrdy defined.
        # self.attributes = [a for a in self.attributes]
        number_of_columns = 2 * (math.ceil(len(self.attributes) / 10))

        column_map = {}
        # you prolly would rather initialize these outside of the function, kuz you're gonna do it twice
        # on this page.
        #self.value_map = {}
        #self.color_map = {}
        for number in range(number_of_columns):
            new_col = QtWidgets.QVBoxLayout()
            column_map[("column" + str(number))] = new_col

        # tal is swedish for number
        for tal in range(len(self.attributes)):
            col_no = 2 * (math.floor(tal / 10))

            new_label = QtWidgets.QLabel(self.attributes[tal] + ":")
            new_button = QtWidgets.QPushButton("-")
            new_pic = QtWidgets.QLabel()
            new_pic.setPixmap(QtGui.QPixmap("pictures/grey.png"))

            # this line shouldn't be needed
            # new_button.clicked.connect(self.assumption_exec)
            if implier == False:
                self.value_map[self.attributes[tal]] = new_button
                self.color_map[self.attributes[tal]] = new_pic
                new_button.clicked.connect(self.alter_value)
            elif implier == True:
                self.implier_value_map[self.attributes[tal]] = new_button
                self.implier_color_map[self.attributes[tal]] = new_pic
                new_button.clicked.connect(self.implier_alter_value)

            new_button.setFixedWidth(40)

            #new_lhbox = QtWidgets.QHBoxLayout()
            #new_lhbox.addStretch()
            #new_lhbox.addWidget(new_label)
            #new_lhbox.addStretch()

            new_hbox = QtWidgets.QHBoxLayout()
            new_hbox.addWidget(new_label)
            new_hbox.addStretch(1)
            new_hbox.addWidget(new_button)
            new_hbox.addWidget(new_pic)
            new_hbox.addStretch()

            #column_map[("column" + str(col_no))].addLayout(new_lhbox)
            column_map[("column" + str(col_no + 1))].addLayout(new_hbox)

        # now to stuff it with filler lines, just so it looks cool :)
        """
        vacuous_lines_needed = len(self.attributes) % 10
        for number in range(vacuous_lines_needed):
            vacuous_label = QtWidgets.QLabel()

            vacuous_hBox = QtWidgets.QHBoxLayout()
            vacuous_hBox.addStretch()
            vacuous_hBox.addWidget(vacuous_label)
            vacuous_hBox.addStretch()

            vacuous_label2 = QtWidgets.QLabel()

            vacuous_lhBox = QtWidgets.QHBoxLayout()
            vacuous_lhBox.addStretch()
            vacuous_lhBox.addWidget(vacuous_label2)
            vacuous_lhBox.addStretch()

            column_map[("column" + str(number_of_columns - 2))].addLayout(vacuous_lhBox)
            column_map[(("column" + str(number_of_columns - 1)))].addLayout(vacuous_hBox)
            """
        for key in column_map:
            recipient_box.addLayout(column_map[key])
            column_map[key].addStretch(1)
        # self.setLayout(self.grand_hbox)

        ## this next line will probably need a little changing ; the implication structure should depend on the inventory
        self.implication_structure = {('high1', True): ('low', False), ('low1', True): ('high', False),
                                      ('front1', True): ('back', False), ('back1', True): ('front', False),
                                      ('approximant1', True): ('sonorant', True),
                                      ('syllabic2', True): ('constrG', False), ('sonorant1', True): ('constrG', False),
                                      ('approximant2', True): ('constrG', False), ('voice1', True): ('constrG', False),
                                      ('spreadG1', True): ('constrG', False), ('continuant1', True): ('constrG', False),
                                      ('constrG1', True): ('spreadG', False), ('lateral1', True): ('consonantal', True),
                                      ('delR1', True): ('consonantal', True), ('delR2', True): ('syllabic', False),
                                      ('delR3', True): ('sonorant', False), ('delR4', True): ('approximant', False),
                                      ('delR5', True): ('nasal', False), ('delR6', True): ('round', False),
                                      ('delR7', True): ('atr', None), ('nasal1', True): ('sonorant', True),
                                      ('nasal2', True): ('approximant', False), ('nasal3', True): ('lateral', False),
                                      ('nasal4', True): ('delR', False), ('nasal5', True): ('strident', False),
                                      ('labial', True): ('coronal', False), ('coronal1', True): ('consonantal', True),
                                      ('coronal2', True): ('labial', False), ('coronal3', True): ('round', False),
                                      ('coronal4', False): ('anterior', None), ('anterior1', True): ('coronal', True),
                                      ('anterior2', False): ('coronal', True),
                                      ('distributed', True): ('consonantal', True), ('strident', True): ('delR', True),
                                      ('dorsal1', False): ('high', None), ('dorsal2', False): ('low', None),
                                      ('dorsal3', False): ('front', None), ('dorsal4', False): ('back', None),
                                      ('dorsal5', False): ('atr', None), ('high2', True): ('dorsal', True),
                                      ('low2', True): ('dorsal', True), ('front2', True): ('dorsal', True),
                                      ('back2', True): ('dorsal', True), ('atr1', True): ('dorsal', True),
                                      ('high3', False): ('dorsal', True), ('low3', False): ('dorsal', True),
                                      ('front3', False): ('dorsal', True), ('back3', False): ('dorsal', True),
                                      ('atr2', False): ('dorsal', True), }

        self.show()

    def alter_value(self):
        sender = self.sender()
        for key in self.value_map:
            if self.value_map[key] == sender:
                color_label = self.color_map[key]
        if sender.text() == '-':
            sender.setText('True')
            color_label.setPixmap(QtGui.QPixmap('pictures/green.png'))
        elif sender.text() == 'True':
            sender.setText('False')
            color_label.setPixmap(QtGui.QPixmap('pictures/red.png'))
        elif sender.text() == 'False':
            sender.setText('Null')
            color_label.setPixmap(QtGui.QPixmap('pictures/yellow.png'))
        elif sender.text() == 'Null':
            sender.setText("-")
            color_label.setPixmap(QtGui.QPixmap('pictures/grey.png'))

    def implier_alter_value(self):
        sender = self.sender()
        for key in self.implier_value_map:
            if self.implier_value_map[key] == sender:
                color_label = self.implier_color_map[key]

        if sender.text() == '-':
            sender.setText('True')
            color_label.setPixmap(QtGui.QPixmap('pictures/green.png'))
        elif sender.text() == 'True':
            sender.setText('False')
            color_label.setPixmap(QtGui.QPixmap('pictures/red.png'))
        elif sender.text() == 'False':
            sender.setText('Null')
            color_label.setPixmap(QtGui.QPixmap('pictures/yellow.png'))
        elif sender.text() == 'Null':
            sender.setText('-')
            color_label.setPixmap(QtGui.QPixmap("pictures/grey.png"))
        ### maybe make it so that you can do have null imply..?

    def add_implication(self):

        # list of consequences for saving is final result, that a key tuple gets mapped into inside the self.implications dictionary
        # self.implier_value_map is a dictionary that links an attribute to a button
        #implications to button map maps the implication (namely, the implying tuple) to the label of the right column used to represent it.

        key_tuple = []
        new_label_text = ""
        was_something_changed = False
        for key in self.implier_value_map:
            if self.implier_value_map[key].text() != "-":
                was_something_changed = True
                # What we want as a result, is a tuple of tuples; that is, a key_tuple full of undertuples.
                undertuple = [key]
                if self.implier_value_map[key].text() == "True":
                    #new_label_text += "+ "
                    undertuple.append(True)
                elif self.implier_value_map[key].text() == "False":
                    #new_label_text += "- "
                    undertuple.append(False)
                elif self.implier_value_map[key].text() == "Null":
                    undertuple.append(None)

                undertuple = tuple(undertuple)
                key_tuple.append(undertuple)

        key_tuple = tuple(key_tuple)

        ## starting off the label text.

        for number in range(len(key_tuple)):
            if number == len(key_tuple)-1 and number == 0:
                if key_tuple[number][1] == True:
                    new_label_text += "+ "
                elif key_tuple[number][1] == False:
                    new_label_text +="- "
                elif key_tuple[number][1] == None:
                    new_label_text += "Null "

                new_label_text += key_tuple[number][0]
            elif number == len(key_tuple) - 1:
                new_label_text += "and "
                if key_tuple[number][1] == True:
                    new_label_text += "+ "
                elif key_tuple[number][1] == False:
                    new_label_text += "- "
                elif key_tuple[number][1] == None:
                    new_label_text += "Null "

                new_label_text += key_tuple[number][0]

            elif number == len(key_tuple) - 2:
                if key_tuple[number][1] == True:
                    new_label_text += "+ "
                elif key_tuple[number][1] == False:
                    new_label_text += "- "
                elif key_tuple[number][1] == None:
                    new_label_text += "Null "

                new_label_text += key_tuple[number][0]
                new_label_text += " "


            else:
                if key_tuple[number][1] == True:
                    new_label_text += "+ "
                elif key_tuple[number][1] == False:
                    new_label_text += "- "
                elif key_tuple[number][1] == None:
                    new_label_text += "Null "
                new_label_text += key_tuple[number][0]
                new_label_text += ", "

        if len(key_tuple)>1:
            new_label_text+= " imply: "
        else:
            new_label_text += " implies: "

        list_of_consequences_for_saving = []
        list_of_consequences = []
        was_something_else_changed = False
        for key in self.value_map:
            if self.value_map[key].text() != "-":
                was_something_else_changed = True
                if self.value_map[key].text() == "True":
                    list_of_consequences.append((key,' + '))
                    list_of_consequences_for_saving.append((key,True))
                elif self.value_map[key].text() == "False":
                    list_of_consequences.append((key,' - '))
                    list_of_consequences_for_saving.append((key,False))
                elif self.value_map[key].text() == "Null":
                    list_of_consequences.append((key,' Null '))
                    list_of_consequences_for_saving.append((key,None))

        for number in range(len(list_of_consequences)):
            if len(list_of_consequences)==1:
                new_label_text += list_of_consequences[number][1]
                new_label_text += list_of_consequences[number][0]
                new_label_text += "."
            elif number == len(list_of_consequences)-1:
                new_label_text += " and "
                new_label_text += list_of_consequences[number][1]
                new_label_text += list_of_consequences[number][0]
                new_label_text += "."
            elif number == len(list_of_consequences)-2:
                new_label_text += list_of_consequences[number][1]
                new_label_text += list_of_consequences[number][0]
            else:
                new_label_text += list_of_consequences[number][1]
                new_label_text += list_of_consequences[number][0]
                new_label_text += ","


        if was_something_changed and was_something_else_changed:
            list_of_consequences_for_saving = tuple(list_of_consequences_for_saving)
            if key_tuple in self.implications:
                
                self.implications_to_button_map[key_tuple].setText(new_label_text)
                
                self.implications[key_tuple] = list_of_consequences_for_saving
                
            else:


                new_label = QtWidgets.QLabel()
                new_label.setText(new_label_text)
                delete_btn = QtWidgets.QPushButton()
                delete_btn.setText("Delete")
                new_label.setWordWrap(True)
                delete_btn.setFixedWidth(50)
                new_label.setFixedWidth(200)
                # ok this if statement helps us make new columns when needed.
                if self.implication_count == 10:
                    #reset the count,
                    self.implication_count = 0
                    # then make a new column :)
                    new_column = QtWidgets.QVBoxLayout()
                    self.target_box = new_column
                    self.main_col_5_H.addLayout(self.target_box)
                else:
                    self.implication_count += 1

                new_hori_box = QtWidgets.QHBoxLayout()
                new_hori_box.addWidget(new_label)
                new_hori_box.addWidget(delete_btn)
                self.target_box.addLayout(new_hori_box)

                #spacer item! this is so they get added from top to bottom, not bottom to top.
                self.target_box.removeItem(self.stretchie)
                self.stretchie = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
                self.target_box.addItem(self.stretchie)
                ## just so you can delete stuff:

                self.delete_btn_label_map[delete_btn] = new_label
                self.delete_button_to_implier_map[delete_btn] = key_tuple
                delete_btn.clicked.connect(self.delete_me)
                self.show()
                # we still need to add stuff in so it actually saves tho
                list_of_consequences_for_saving = tuple(list_of_consequences_for_saving)
                self.implications[key_tuple] = list_of_consequences_for_saving
                self.implications_to_button_map[key_tuple]=new_label

    def add_implication_old(self):
        key_tuple = [" ",None]
        new_label_text = ""
        was_something_changed = False
        for key in self.implier_value_map:
            if self.implier_value_map[key].text() != "Null":
                was_something_changed = True
                if self.implier_value_map[key].text() == "True":
                    new_label_text += "+ "
                    key_tuple[1] = True
                elif self.implier_value_map[key].text() == "False":
                    new_label_text += "- "
                    key_tuple[1] = False
                key_tuple[0] = key
                new_label_text += key
                new_label_text += " implies: "
        key_tuple = tuple(key_tuple)
        list_of_consequences_for_saving = []
        list_of_consequences = []
        was_something_else_changed = False
        for key in self.value_map:
            if self.value_map[key].text() != "Null":
                was_something_else_changed = True
                if self.value_map[key].text() == "True":
                    list_of_consequences.append((key,' + '))
                    list_of_consequences_for_saving.append((key,True))
                elif self.value_map[key].text() == "False":
                    list_of_consequences.append((key,' - '))
                    list_of_consequences_for_saving.append((key,False))
        for consequence in list_of_consequences:
            new_label_text += consequence[1]
            new_label_text += consequence[0]

        if was_something_changed and was_something_else_changed:
            list_of_consequences_for_saving = tuple(list_of_consequences_for_saving)
            if key_tuple in self.implications:
                
                self.implications_to_button_map[key_tuple].setText(new_label_text)
                
                self.implications[key_tuple] = list_of_consequences_for_saving
                
            else:


                new_label = QtWidgets.QLabel()
                new_label.setText(new_label_text)
                delete_btn = QtWidgets.QPushButton()
                delete_btn.setText("Delete")
                new_label.setWordWrap(True)
                delete_btn.setFixedWidth(50)
                new_label.setFixedWidth(200)
                # ok this if statement helps us make new columns when needed.
                if self.implication_count == 10:
                    #reset the count,
                    self.implication_count = 0
                    # then make a new column :)
                    new_column = QtWidgets.QVBoxLayout()
                    self.target_box = new_column
                    self.main_col_5_H.addLayout(self.target_box)
                    self.stretchie = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
                    self.target_box.addItem(self.stretchie)
                else:
                    self.implication_count += 1

                new_hori_box = QtWidgets.QHBoxLayout()
                new_hori_box.addWidget(new_label)
                new_hori_box.addWidget(delete_btn)
                self.target_box.addLayout(new_hori_box)

                ## just so you can delete stuff:

                self.delete_btn_label_map[delete_btn] = new_label
                self.delete_button_to_implier_map[delete_btn] = key_tuple
                delete_btn.clicked.connect(self.delete_me)
                self.show()
                # we still need to add stuff in so it actually saves tho
                list_of_consequences_for_saving = tuple(list_of_consequences_for_saving)
                self.implications[key_tuple] = list_of_consequences_for_saving
                self.implications_to_button_map[key_tuple]=new_label

                self.target_box.removeItem(self.stretchie)
                self.stretchie = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
                self.target_box.addItem(self.stretchie)
        else:
            hey_man = QtWidgets.QMessageBox.warning(self, "Specification Needed",
                                                    "You Need to Select an Attribute to the Left that Entails Attributes on the Right",
                                                    QMessageBox.Ok)

    def delete_me(self):
        self.sender().hide()
        if self.implication_count > 0:
            self.implication_count -= 1
        self.delete_btn_label_map[self.sender()].hide()
        key_tuple = self.delete_button_to_implier_map[self.sender()]
        
        self.implications.pop(key_tuple,None)

    def show_what_we_already_got(self):
        # this function makes sure we start off with all of the entailments already in the system
        implications = technical_map[self.chosenInventory]["Entailments"]
        self.implications = implications
        
        
        
        # ok now just building the string of text we want
        for key in implications:
            label_text = ""
            
            for number in range(len(key)):
                if len(key) == 1:
                    if key[number][1] == True:
                        label_text += "+ "
                    elif key[number][1] == False:
                        label_text += "- "
                    elif key[number][1] == None:
                        label_text += "Null "
                    label_text += key[number][0]
                elif number == len(key) - 1:
                    label_text += "and "
                    if key[number][1] == True:
                        label_text += "+ "
                    elif key[number][1] == False:
                        label_text += "- "
                    elif key[number][1] == None:
                        label_text += "Null "
                    label_text += key[number][0]
                elif number == len(key) - 2:
                    if key[number][1] == True:
                        label_text += "+ "
                    elif key[number][1] == False:
                        label_text += "- "
                    elif key[number][1] == None:
                        label_text += "Null "
                    label_text += key[number][0]
                    label_text += " "
                else:
                    if key[number][1] == True:
                        label_text += "+ "
                    elif key[number][1] == False:
                        label_text += "- "
                    elif key[number][1] == None:
                        label_text += "Null "
                    label_text += key[number][0]
                    label_text += ", "
            
            if len(key) == 1:
                label_text += " implies : "
            else:
                label_text += " imply : "

            for entailed in implications[key]:

                if entailed[1] == True:
                    label_text += "+ "
                elif entailed[1] == False:
                    label_text += "- "
                else:
                    label_text += "Null "

                label_text += entailed[0]

            new_label = QtWidgets.QLabel()
            new_label.setText(label_text)
            delete_btn = QtWidgets.QPushButton()
            delete_btn.setText("Delete")
            new_label.setWordWrap(True)
            delete_btn.setFixedWidth(50)
            new_label.setFixedWidth(200)
            # ok this if statement helps us make new columns when needed.
            if self.implication_count == 10:
                # reset the count,
                self.implication_count = 0
                # then make a new column :)
                new_column = QtWidgets.QVBoxLayout()
                self.target_box = new_column
                self.target_box.addStretch(0)
                self.main_col_5_H.addLayout(self.target_box)
            else:
                self.implication_count += 1

            new_hori_box = QtWidgets.QHBoxLayout()
            new_hori_box.addWidget(new_label)
            new_hori_box.addWidget(delete_btn)
            self.target_box.addLayout(new_hori_box)

            ## just so you can delete stuff:

            self.delete_btn_label_map[delete_btn] = new_label
            self.delete_button_to_implier_map[delete_btn] = key
            delete_btn.clicked.connect(self.delete_me)
            self.show()
            # we still need to add stuff in so it actually saves tho
            self.implications_to_button_map[key] = new_label

           # spacer!
            self.target_box.removeItem(self.stretchie)
            self.stretchie = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.target_box.addItem(self.stretchie)

    def show_what_we_already_got_old(self):
        # this function makes sure we start off with all of the entailments already in the system
        implications = technical_map[self.chosenInventory]["Entailments"]
        self.implications = implications
        
        
        
        print (technical_map)
        for entailment in implications:

            
            
            if entailment[1] == True:
                label_text = "+ "
            else:
                label_text = "- "

            label_text += entailment[0]
            label_text += " entails : "

            for entailed in implications[entailment]:
                
                
                if entailed[1] == True:
                    label_text += "+ "
                else:
                    label_text += "- "

                label_text += entailed[0]

            new_label = QtWidgets.QLabel()
            new_label.setText(label_text)
            delete_btn = QtWidgets.QPushButton()
            delete_btn.setText("Delete")
            new_label.setWordWrap(True)
            delete_btn.setFixedWidth(50)
            new_label.setFixedWidth(200)
            # ok this if statement helps us make new columns when needed.
            if self.implication_count == 10:
                # reset the count,
                self.implication_count = 0
                # then make a new column :)
                new_column = QtWidgets.QVBoxLayout()
                self.target_box = new_column
                self.target_box.addStretch(0)
                self.main_col_5_H.addLayout(self.target_box)
            else:
                self.implication_count += 1

            new_hori_box = QtWidgets.QHBoxLayout()
            new_hori_box.addWidget(new_label)
            new_hori_box.addWidget(delete_btn)
            self.target_box.addLayout(new_hori_box)

            ## just so you can delete stuff:

            self.delete_btn_label_map[delete_btn] = new_label
            self.delete_button_to_implier_map[delete_btn] = entailment
            delete_btn.clicked.connect(self.delete_me)
            self.show()
            # we still need to add stuff in so it actually saves tho
            self.implications_to_button_map[entailment] = new_label

           # spacer!
            self.target_box.removeItem(self.stretchie)
            self.stretchie = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.target_box.addItem(self.stretchie)

    def save_it_all(self):
        hey_man = QMessageBox.question(self,"Save?","Are you sure you want to finish and save your work?",QMessageBox.Yes|QMessageBox.No)

        if hey_man == QMessageBox.No:
            pass
        else:
            technical_map[self.chosenInventory]["Entailments"] = self.implications
            self.parent.close()
            self.close()

class data_transfer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle("Transfer Data")
        self.setWindowIcon(QIcon('pictures/transfer.png'))
    def init_ui(self):



        self.grandVbox = QtWidgets.QVBoxLayout()

        self.logo = QtGui.QPixmap('pictures/transfer.png')
        self.logo = self.logo.scaled(250, 125, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.picture = QtWidgets.QLabel()
        self.picture.setPixmap(self.logo)

        self.grandVbox.addWidget(self.picture)

        self.h_box1 = QtWidgets.QHBoxLayout()
        self.h_box1.addStretch()
        self.export_label = QtWidgets.QLabel("Export From")
        self.h_box1.addWidget(self.export_label)
        self.dump_label = QtWidgets.QLabel("Import to")
        self.h_box1.addWidget(self.dump_label)
        self.h_box1.addStretch()

        self.h_box2 = QtWidgets.QHBoxLayout()
        self.h_box2.addStretch()
        self.export_box = QComboBox()
        self.export_box.addItem("Null")
        self.import_box = QComboBox()
        self.import_box.addItem("Null")
        self.h_box2.addWidget(self.export_box)
        self.h_box2.addWidget(self.import_box)
        self.h_box2.addStretch()

        for key in feature_set_map:
            self.export_box.addItem(key)
            self.import_box.addItem(key)

        self.import_phonemes = QCheckBox()
        self.import_phonemes.setText("Import Phonemes")
        self.import_feature_groups = QCheckBox()
        self.import_feature_groups.setText("Import Feature Groups")
        self.import_entailments = QCheckBox()
        self.import_entailments.setText("Import Entailments")
        self.import_languages = QCheckBox()
        self.import_languages.setText("Import Language Inventories")

        self.transfer_btn = QtWidgets.QPushButton()
        self.transfer_btn.setText("Transfer")
        self.transfer_btn.clicked.connect(self.transfer_data)

        self.grandVbox.addLayout(self.h_box1)
        self.grandVbox.addLayout(self.h_box2)
        self.grandVbox.addWidget(self.import_phonemes)
        self.grandVbox.addWidget(self.import_feature_groups)
        self.grandVbox.addWidget(self.import_entailments)
        self.grandVbox.addWidget(self.import_languages)
        self.grandVbox.addWidget(self.transfer_btn)

        self.setLayout(self.grandVbox)
        self.show()


    def transfer_data(self):

        export_features = feature_set_map[self.export_box.currentText()]
        import_features = feature_set_map[self.import_box.currentText()]

        if self.import_phonemes.isChecked() == True:

            # finnish for those to be transferred
            siirrettäviä = [a for a in dictionish[self.export_box.currentText()]]
            # finnish for those to be acccepted
            vastaan_otettavia = [a for a in dictionish[self.import_box.currentText()]]


            ## Now to see if there will be any phonemes with the same name.

            # the names of those to be transferred
            siirrettävien_nimet = [a for a in inventories[self.export_box.currentText()]["All Phonemes"]]
            vastaan_otettavien_nimet = [a for a in inventories[self.import_box.currentText()]["All Phonemes"]]
            toistettuja = []
            for foneemi in siirrettävien_nimet:
                if foneemi in vastaan_otettavien_nimet:
                    toistettuja.append(foneemi)

            overwrite = False
            side_by_side = False
            skip = False
            if len(toistettuja) > 0:
                hey_man = save_options(self)

                if hey_man.pop_up.clickedButton().text() == "Overwrite":
                    overwrite = True
                elif hey_man.pop_up.clickedButton().text() == "Import Side by Side":
                    side_by_side= True
                elif hey_man.pop_up.clickedButton().text() == "Skip":
                    skip = True
                else:
                    return None


            if side_by_side == True:
                for phoneme in siirrettäviä:
                    remake = []
                    remake_necessaary = False
                    for attribute in phoneme:
                        if attribute[0] == "name" and attribute[1] in toistettuja:
                            remake_necessaary = True
                            remake.append(("name",attribute[1]+"_2"))
                            siirrettävien_nimet = [a for a in siirrettävien_nimet if a != attribute[1]]
                            siirrettävien_nimet.append((attribute[1]+"_2"))
                        else:
                            remake.append(attribute)


                    if remake_necessaary == True:
                        siirrettäviä = [a for a in siirrettäviä if a != phoneme]
                        remake = tuple(remake)
                        siirrettäviä.append(remake)
                    else:
                        pass

            elif skip == True:
                for phoneme in siirrettäviä:
                    for attribute in phoneme:
                        if attribute[0]=="name" and attribute[1] in toistettuja:
                            siirrettäviä = [a for a in siirrettäviä if a != phoneme]
            else:
                pass


            ### ok, now we have to transfer the data from one format to another.

            siirrettyjä = []

            for phoneme in siirrettäviä:

                remake = []

                for attribute in phoneme:


                    if attribute[0] == "name" or attribute[0] in import_features:
                        remake.append(attribute)
                        #

                    else:
                        pass

                

                
                
                
                

                for feature in import_features:
                    if feature not in export_features:
                        remake.append((feature,None))
                        

                remake = tuple(remake)
                
                siirrettyjä.append(remake)

            for old_phoneme in dictionish[self.import_box.currentText()]:
                siirrettyjä.append(old_phoneme)
            dictionish[self.import_box.currentText()] = siirrettyjä
            for nimi in siirrettävien_nimet:
                inventories[self.import_box.currentText()]["All Phonemes"].append(nimi)

            ## does the order in which they are appended matter?

            ## ok, now to see if we're transferring other bits of data.
            pop_me = []

            pop_me = []

            if self.import_languages.isChecked() == True:
                for inventory in inventories[self.export_box.currentText()]:
                    if inventory != "All Phonemes":
                        inventories[self.import_box.currentText()][inventory] = \
                        inventories[self.export_box.currentText()][inventory]
                    else:
                        pass

        if self.import_entailments.isChecked() == True:
            siirrettäviä_seuraamuksia = {}
            export_entailments = {}
            for entry in technical_map[self.export_box.currentText()]["Entailments"]:
                export_entailments[entry] = technical_map[self.export_box.currentText()]["Entailments"][entry]
            for impKey in export_entailments:
                importable = True
                for subkey in impKey:
                    if subkey[0] not in import_features:
                        print("this is the subkey: %s , and these are the import features : %s"%(subkey[0],import_features))
                        importable = False
                for consequence in export_entailments[impKey]:
                    if consequence[0] not in import_features:
                        print("this is the consequence: %s , and these are the import features : %s" % (
                        consequence[0], import_features))
                        importable = False

                if importable == True:
                    siirrettäviä_seuraamuksia[impKey] = export_entailments[impKey]
                else:
                    #At this point, it's already been decided that it's not going to work.
                    entailment_statement = "\" "
                    for number in range(len(impKey)):
                        
                        
                        if len(impKey) == 1:
                            if impKey[number][1] == True:
                                entailment_statement += "+ "
                            elif impKey[number][1]==False:
                                entailment_statement += "- "
                            else:
                                entailment_statement += "Null "
                            entailment_statement += impKey[number][0]
                            entailment_statement += " entails "
                        elif number == len(impKey) -1:
                            entailment_statement += "and "
                            if impKey[number][1] == True:
                                entailment_statement += "+ "
                            elif impKey[number][1] == False:
                                entailment_statement += "- "
                            else:
                                entailment_statement += "Null "
                            entailment_statement += impKey[number][0]
                            entailment_statement += " entail "
                        elif number == len(impKey)-2:

                            if impKey[number][1] == True:
                                entailment_statement += "+ "
                            elif impKey[number][1] == False:
                                entailment_statement += "- "
                            else:
                                entailment_statement += "Null "
                            entailment_statement += impKey[number][0]
                            entailment_statement += " "
                        else:
                            if impKey[number][1] == True:
                                entailment_statement += "+ "
                            elif impKey[number][1] == False:
                                entailment_statement += "- "
                            else:
                                entailment_statement += "Null "
                                entailment_statement += impKey[number][0]
                                entailment_statement += ", "


                    consequences = export_entailments[impKey]
                    for number in range(len(consequences)):
                        if len(consequences) == 1:
                            if consequences[number][1] == True:
                                entailment_statement += "+ "
                            elif consequences[number][1]==False:
                                entailment_statement += "- "
                            else:
                                entailment_statement += "Null "
                            entailment_statement += consequences[number][0]
                        elif number == len(consequences) -1:
                            entailment_statement += "and "

                            if consequences[number][1] == True:
                                entailment_statement += "+ "
                            elif consequences[number][1] == False:
                                entailment_statement += "- "
                            else:
                                entailment_statement += "Null "
                            entailment_statement += consequences[number][0]
                            entailment_statement += "entail "
                        elif number == len(consequences)-2:

                            if consequences[number][1] == True:
                                entailment_statement += "+ "
                            elif consequences[number][1] == False:
                                entailment_statement += "- "
                            else:
                                entailment_statement += "Null "
                            entailment_statement += consequences[number][0]
                            entailment_statement += " "
                        else:
                            if consequences[number][1] == True:
                                entailment_statement += "+ "
                            elif consequences[number][1] == False:
                                entailment_statement += "- "
                            else:
                                entailment_statement += "Null "
                                entailment_statement += consequences[number][0]
                                entailment_statement += ", "

                    entailment_statement += " \" "

                    hey_man = QtWidgets.QMessageBox.warning(self, "Unable to Import Entailment",
                                                            "The entailment %s could not be imported due to incompatabile attributes."%entailment_statement,
                                                            QMessageBox.Ok)

                technical_map[self.import_box.currentText()]["Entailments"] = siirrettäviä_seuraamuksia
            #  I think I'm going to redo this part of the code. This udner here is the old section.
            # for onsies, I think if an incoming entailment has an incompatible feature, it's better to just bag it all together.
            """
            siirrettäviä_seuraamuksia = technical_map[self.export_box.currentText()]["Entailments"]
            
            for seuraamus in siirrettäviä_seuraamuksia:
                remake = []
                remake_necessaary = False

                if seuraamus[0] not in import_features:
                    pop_me.append(seuraamus)

                else:
                    for ominaisuus in siirrettäviä_seuraamuksia[seuraamus]:
                        if ominaisuus[0] not in import_features:
                            remake_necessaary = True
                        else:
                            remake.append(ominaisuus)

                    if remake_necessaary == True:
                        remake = tuple(remake)
                        siirrettäviä_seuraamuksia[seuraamus] = remake
                    else:
                        pass

            for popable in pop_me:
                siirrettäviä_seuraamuksia.pop(popable, None)
            technical_map[self.import_box.currentText()]["Entailments"] = siirrettäviä_seuraamuksia
            """
        if self.import_feature_groups.isChecked() == True:
            ## finnish for "transferred featuregroups"
            pop_me = []
            
            siirrettyjä_ominaisuus_ryhmiä = {}
            for key in technical_map[self.export_box.currentText()]["keyCategories"]:
                siirrettyjä_ominaisuus_ryhmiä[key] = technical_map[self.export_box.currentText()]["keyCategories"][key]
            
            for key in siirrettyjä_ominaisuus_ryhmiä:
                
                
                remake = []
                remake_necessaary = False
                for ominaisuus in siirrettyjä_ominaisuus_ryhmiä[key]:
                    
                    if ominaisuus[0] not in import_features:
                        
                        
                        remake_necessaary = True
                    else:
                        remake.append(ominaisuus)

                if remake_necessaary == True and len(remake) > 0:
                    
                    siirrettyjä_ominaisuus_ryhmiä[key] = tuple(remake)
                    hey_man = QtWidgets.QMessageBox.warning(self, "Must Import Phonemes",
                                                            "The feature group named %s was altered during import due to an incompatible attribute" % key,
                                                            QMessageBox.Ok)
                elif remake_necessaary == True and len(remake) == 0:
                    
                    
                    
                    pop_me.append(key)
                    hey_man = QtWidgets.QMessageBox.warning(self, "Must Import Phonemes",
                                                            "Unable to import the feature group named %s due to an incompatible attribute"%key,
                                                            QMessageBox.Ok)
                else:
                    
                    pass
            
            for popable in pop_me:
                siirrettyjä_ominaisuus_ryhmiä.pop(popable, None)
            
            
            technical_map[self.import_box.currentText()]["keyCategories"] = siirrettyjä_ominaisuus_ryhmiä
            

            
        if self.import_languages.isChecked() == True and self.import_phonemes.isChecked() == False:

            hey_man = QtWidgets.QMessageBox.warning(self, "Must Import Phonemes",
                                                    "In order to import the languages, you must click import phonemes. If you would like to import the languages of one feature set to another without modifying the phonemes of another, you may select \"skip\" when asked what to do about redundant phonemes.",
                                                    QMessageBox.Ok)


        
        hey_man = QtWidgets.QMessageBox.warning(self,"Done Saving","You have successfully saved the data from the %s inventory to the %s inventory"%(self.export_box.currentText(),self.import_box.currentText()),QMessageBox.Ok)
        
        reset_phoneme_map()
        
        inventory_update.set_off()
        
        #
        #
        #
        #

        self.close()


class alter_group_of_phonemes_opening_page(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.page2 = alter_goup_of_phonemes(self)
        self.layout = QtWidgets.QVBoxLayout()
        self.logo = QtGui.QPixmap('pictures/edit phoneme group.png')
        self.logo = self.logo.scaled(250,150,Qt.IgnoreAspectRatio,Qt.FastTransformation)
        self.picture = QtWidgets.QLabel()
        self.picture.setPixmap(self.logo)
        self.picture.setFixedWidth(250)
        self.layout.addWidget(self.picture)
        self.prompt = QtWidgets.QLabel("Choose a Featureset")
        self.layout.addWidget(self.prompt)
        self.choose_box = QtWidgets.QComboBox()
        self.choose_box.addItem("Null")
        for key in feature_set_map:
            self.choose_box.addItem(key)
        self.layout.addWidget(self.choose_box)
        self.next_btn = QtWidgets.QPushButton("Next")
        self.next_btn.clicked.connect(self.next_page)
        self.layout.addWidget(self.next_btn)
        self.setLayout(self.layout)

        self.setWindowTitle("Edit a Group of Phonemes")
        self.setWindowIcon(QtGui.QIcon('pictures/edit phoneme group.png'))
        self.show()

    def next_page(self):
        if self.choose_box.currentText() == "Null":
            hey_man = QtWidgets.QMessageBox.warning(self, "Choose A Feature Set",
                                                    "You Need to Select a Feature-Set First.",
                                                    QMessageBox.Ok)
        else:
            self.page2.chosenInventory = self.choose_box.currentText()
            self.page2.init_ui()
            self.page2.fill_it_all_out()
            self.page2.show()



class alter_goup_of_phonemes(QtWidgets.QWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.chosenInventory = "Null"
        self.grand_hbox =QtWidgets.QHBoxLayout()
        self.init_ui
    def init_ui(self):

        

        self.setWindowTitle("Alter Group of Phonemes")
        self.setWindowIcon(QtGui.QIcon("pictures/edit phoneme group"))
        self.grandVbox = QtWidgets.QVBoxLayout()

        self.h_box1 = QtWidgets.QHBoxLayout()
        self.v_box1 = QtWidgets.QVBoxLayout()
        self.v_box2 = QtWidgets.QVBoxLayout()
        #self.grand_hbox = QtWidgets.QHBoxLayout()
        self.v_box2.addLayout(self.grand_hbox)
        self.h_box1.addLayout(self.v_box1)
        self.h_box1.addLayout(self.v_box2)
        self.h_box_mini_1 = QtWidgets.QHBoxLayout()
        self.v_box1.addLayout(self.h_box_mini_1)
        self.h_box2 = QtWidgets.QHBoxLayout()

        self.grandVbox.addLayout(self.h_box1)
        self.grandVbox.addLayout(self.h_box2)

        

        self.instructions = QtWidgets.QLabel("Enter Phonemes Here:")
        self.assistive_click = QtWidgets.QPushButton()
        self.assistive_click.setText("Assistive Click")
        self.assistive_click.clicked.connect(self.show_assistive_click)

        self.entry_box = QtWidgets.QTextEdit()
        self.change_btn = QtWidgets.QPushButton()
        self.change_btn.setText("Save Changes")
        self.change_btn.clicked.connect(self.save_changes)
        self.feature_assumption_toggle = QtWidgets.QCheckBox()
        self.feature_assumption_toggle.setText("Toggle Assume Entailments")
        
        self.feature_assumption_toggle.clicked.connect(self.recursive_assume)



        self.h_box_mini_1.addWidget(self.instructions)
        self.h_box_mini_1.addWidget(self.assistive_click)
        self.v_box1.addWidget(self.feature_assumption_toggle)
        self.v_box1.addWidget(self.entry_box)
        self.grandVbox.addWidget(self.change_btn)

        self.setLayout(self.grandVbox)
        self.value_map = {}
        self.show()

    def recursive_assume(self,the_sender = None):
        
        
        if self.feature_assumption_toggle.isChecked():

            for impKey in technical_map[self.chosenInventory]["Entailments"]:
                
                it_could_apply = True
                iteration = 0
                while it_could_apply and iteration < len(impKey):
                    comparative_value =""
                    if self.value_map[impKey[iteration][0]].text() == "Null":
                        comparative_value = 'None'
                    else:
                        comparative_value = self.value_map[impKey[iteration][0]].text()

                    if comparative_value != str(impKey[iteration][1]):
                        
                        it_could_apply = False
                    iteration+=1
                
                if it_could_apply:
                    it_does_apply = True
                else:
                    it_does_apply = False
                if it_does_apply:

                    #We have to define the variables in two steps because of an ambiguity in python;
                    # if a tuple is a key in a dictionary to an iterable thing, it picks the wrong things.

                    ## this half of the code executes the necessary changes. the previous half is identifying if u need to do anything

                    questioned_features = technical_map[self.chosenInventory]["Entailments"][impKey]
                    
                    # questioned eatures is a tuple of tuples

                    for questioned_feature in questioned_features:

                        

                        consequent_feature_value = str(questioned_feature[1])
                        
                        current_feature_value = self.value_map[questioned_feature[0]].text()
                        
                        #questioned feature is the one that should get changed - in this case, sonorancy
                        #consequent feature value is what sonarancy should have, and current feature value is what it does currently have.
                        if current_feature_value == "Null":
                            current_feature_value="None"
                        if consequent_feature_value != current_feature_value:
                            if consequent_feature_value == 'True' or consequent_feature_value == 'False':
                                self.value_map[questioned_feature[0]].setText(consequent_feature_value)
                            elif consequent_feature_value == 'None':
                                self.value_map[questioned_feature[0]].setText('Null')
                            colorswab = self.color_map[questioned_feature[0]]
                            if consequent_feature_value == 'None':
                                colorswab.setPixmap(QtGui.QPixmap('pictures/grey.png'))
                            elif consequent_feature_value == 'True':
                                colorswab.setPixmap(QtGui.QPixmap('pictures/green.png'))
                            elif consequent_feature_value == 'False':
                                colorswab.setPixmap(QtGui.QPixmap('pictures/red.png'))
                            did_it_go = True
                        
                        

                        ## use this to find out if the sender was the one who got changed... incomplete
                        the_senders_attribute = None
                        if the_sender != None and isinstance(the_sender,QtWidgets.QPushButton):
                            for attribute in self.value_map:
                                if self.value_map[attribute] == the_sender:
                                    the_senders_attribute = attribute
                                    break
                            
                            
                            
                            ## what's going on here, is the_sender's text is it's null/+/- value, not it's attribute
                            if questioned_feature[0] == the_senders_attribute:
                                implying_statement = ""
                                for number in range(len(impKey)):
                                    if number == len(impKey) -1 and number > 0:
                                        implying_statement += "and "
                                    if impKey[number][1] == True:
                                        implying_statement += "+ "
                                    elif impKey[number][1] == False:
                                        implying_statement += "- "
                                    elif impKey[number][1] == None:
                                        implying_statement += "Null "
                                    implying_statement += impKey[number][0]
                                    if number < len(impKey)-2:
                                        implying_statement += ", "
                                    else:
                                        implying_statement += " "
                                    if len(impKey) == 1:
                                        implying_statement += "entails "
                                    else:
                                        implying_statement += "entail "

                                hey_man = QMessageBox.warning(self, "Cannot Change", "%s that the %s feature must have it's current value."%(implying_statement,the_senders_attribute),
                                                              QMessageBox.Ok)

                # this recursivity may not be needed

        else:
            pass


    def recursive_assume_old(self):
        if self.feature_assumption_toggle.isChecked():
            did_it_go = False
            for key in self.value_map:
                for impKey in self.implication_structure:
                    if key in impKey[0]:
                        if self.value_map[key].text() == str(impKey[1]):
                            questioned_feature = self.implication_structure[impKey][0]
                            consequent_feature_value = str(self.implication_structure[impKey][1])
                            current_feature_value = self.value_map[questioned_feature].text()
                            if current_feature_value == "Null":
                                current_feature_value = "None"
                            if consequent_feature_value != current_feature_value:
                                if consequent_feature_value == 'True' or consequent_feature_value == 'False':
                                    self.value_map[questioned_feature].setText(consequent_feature_value)
                                elif consequent_feature_value == 'None':
                                    self.value_map[questioned_feature].setText('Null')
                                colorswab = self.color_map[questioned_feature]
                                if consequent_feature_value == 'None':
                                    colorswab.setPixmap(QtGui.QPixmap('pictures/grey.png'))
                                elif consequent_feature_value == 'True':
                                    colorswab.setPixmap(QtGui.QPixmap('pictures/green.png'))
                                elif consequent_feature_value == 'False':
                                    colorswab.setPixmap(QtGui.QPixmap('pictures/red.png'))
                                did_it_go = True

                if did_it_go == True:
                    self.recursive_assume()
                else:
                    pass
        else:
            pass

    def show_assistive_click(self):
        self.asistive_click_window =assistive_click(self,self.entry_box,self.parent.choose_box.currentText(),"All Phonemes")

    def alter_value(self):
        sender = self.sender()
        for key in self.value_map:
            if self.value_map[key] == sender:
                color_label = self.color_map[key]
        if sender.text() == 'Null':
            sender.setText('True')
            color_label.setPixmap(QtGui.QPixmap('pictures/green.png'))
        elif sender.text() == 'True':
            sender.setText('False')
            color_label.setPixmap(QtGui.QPixmap('pictures/red.png'))
        elif sender.text() == 'False':
            sender.setText('To Null')
            color_label.setPixmap(QtGui.QPixmap('pictures/yellow.png'))
        elif sender.text() == "To Null":
            sender.setText('Null')
            color_label.setPixmap(QtGui.QPixmap('pictures/grey.png'))
    def assumption_exec(self):
        def assumption(beclicked):
            did_it_go=False
            sender = beclicked
            # OK, I'll be honest, the need for this next line of code defining key is a little weird.
            # without it, the program will still work properly but one of the threads will run an error saying
            # that key is referenced before its assignment. I have no idea why.
            key = 'consonantal'
            for attribute in self.value_map:
                if self.value_map[attribute] == sender:
                    key = attribute
                    break
            for impKey in self.implication_structure:
                if key in impKey[0]:

                    if self.value_map[key].text() == str(impKey[1]):
                        questioned_feature = self.implication_structure[impKey][0]
                        consequent_feature_value = str(self.implication_structure[impKey][1])
                        if consequent_feature_value != self.value_map[questioned_feature].text():
                            if consequent_feature_value == 'True'or consequent_feature_value == 'False':
                                self.value_map[questioned_feature].setText(consequent_feature_value)
                            elif consequent_feature_value == 'None':
                                self.value_map[questioned_feature].setText('Null')
                            colorswab = self.color_map[questioned_feature]
                            if consequent_feature_value == 'None':
                                colorswab.setPixmap(QtGui.QPixmap('pictures/grey.png'))
                            elif consequent_feature_value == 'True':
                                colorswab.setPixmap(QtGui.QPixmap('pictures/green.png'))
                            elif consequent_feature_value == 'False':
                                colorswab.setPixmap(QtGui.QPixmap('pictures/red.png'))
                            did_it_go= True

            if did_it_go == True:
                assumption(self.sender())
            else:
                pass
        if self.feature_assumption_toggle.isChecked():
            timer = Timer(2, assumption, [self.sender()])
            timer.start()
        else:
            pass

    def fill_it_all_out(self):
        # code for resetting the thing here
        # for luku in range (1,self.grand_hbox.count()):
        #     self.grand_hbox.removeItem(self.grand_hbox.itemAt(luku))
        #     
        #

        # I think I was right in changing the right side from self.chooseFeatureset.currentText() to nothing
        # and then having the next page button define it.
        #self.chosenInventory = self.chooseFeatureSet.currentText()

        ## ok this line needed to be changed. I want to get the attributes from the class tuples thing instead, that's neater
        #self.attributes = [a for a in set_map[self.chosenInventory]["All Phonemes"][0].attributes]
        for key in feature_set_map:
            
            if key == self.parent.choose_box.currentText():
                
                self.attributes = feature_set_map[key]

        number_of_columns = 2*(math.ceil(len(self.attributes)/10))

        column_map = {}
        self.value_map = {}
        self.color_map = {}
        for number in range(number_of_columns):
            new_col = QtWidgets.QVBoxLayout()
            column_map[("column"+str(number))]= new_col

        # tal is swedish for number
        for tal in range(len(self.attributes)):
            col_no = 2*(math.floor(tal/10))

            new_label = QtWidgets.QLabel(self.attributes[tal]+":")
            new_button= QtWidgets.QPushButton("Null")
            new_pic  = QtWidgets.QLabel()
            new_pic.setPixmap(QtGui.QPixmap("pictures/grey.png"))
            new_button.clicked.connect(self.alter_value)
            new_button.clicked.connect(partial(self.recursive_assume,new_button))

            self.value_map[self.attributes[tal]] = new_button
            self.color_map[self.attributes[tal]] = new_pic

            new_lhbox = QtWidgets.QHBoxLayout()
            new_lhbox.addStretch()
            new_lhbox.addWidget(new_label)
            new_lhbox.addStretch()

            new_hbox = QtWidgets.QHBoxLayout()
            new_hbox.addStretch()
            new_hbox.addWidget(new_button)
            new_hbox.addWidget(new_pic)
            new_hbox.addStretch()

            column_map[("column"+str(col_no))].addLayout(new_lhbox)
            column_map[("column" + str(col_no+1))].addLayout(new_hbox)

        # now to stuff it with filler lines, just so it looks cool :)

        vacuous_lines_needed = len(self.attributes)%10
        for number in range(vacuous_lines_needed):
            vacuous_label = QtWidgets.QLabel()

            vacuous_hBox = QtWidgets.QHBoxLayout()
            vacuous_hBox.addStretch()
            vacuous_hBox.addWidget(vacuous_label)
            vacuous_hBox.addStretch()

            vacuous_label2 = QtWidgets.QLabel()

            vacuous_lhBox = QtWidgets.QHBoxLayout()
            vacuous_lhBox.addStretch()
            vacuous_lhBox.addWidget(vacuous_label2)
            vacuous_lhBox.addStretch()



            column_map[("column"+str(number_of_columns-2))].addLayout(vacuous_lhBox)
            column_map[(("column"+str(number_of_columns-1)))].addLayout(vacuous_hBox)

        for key in column_map:
            self.grand_hbox.addLayout(column_map[key])
        #self.setLayout(self.grand_hbox)


            ## this next line will probably need a little changing ; the implication structure should depend on the inventory
        self.implication_structure = {('high1',True):('low',False),('low1',True):('high',False),('front1',True):('back',False),('back1',True):('front',False),
                                      ('approximant1',True):('sonorant',True),
                                      ('syllabic2',True):('constrG',False),('sonorant1',True):('constrG',False),
                                      ('approximant2',True):('constrG',False),('voice1',True):('constrG',False),
                                      ('spreadG1',True):('constrG',False),('continuant1',True):('constrG',False),
                                      ('constrG1',True):('spreadG',False),('lateral1',True):('consonantal',True),
                                      ('delR1',True):('consonantal',True),('delR2',True):('syllabic',False),
                                      ('delR3', True): ('sonorant', False),('delR4',True):('approximant',False),
                                      ('delR5',True):('nasal',False),('delR6', True): ('round', False),
                                      ('delR7',True):('atr',None),('nasal1',True):('sonorant',True),
                                      ('nasal2',True):('approximant',False),('nasal3',True):('lateral',False),
                                      ('nasal4',True):('delR',False),('nasal5',True):('strident',False),
                                      ('labial',True):('coronal',False),('coronal1',True):('consonantal',True),
                                      ('coronal2',True):('labial',False),('coronal3',True):('round',False),
                                      ('coronal4',False):('anterior',None),('anterior1',True):('coronal',True),('anterior2',False):('coronal',True),
                                      ('distributed',True):('consonantal',True),('strident',True):('delR',True),
                                      ('dorsal1',False):('high',None),('dorsal2', False): ('low', None),
                                      ('dorsal3',False):('front',None),('dorsal4',False):('back',None),
                                      ('dorsal5',False):('atr',None),('high2',True):('dorsal',True),
                                      ('low2',True):('dorsal',True),('front2',True):('dorsal',True),
                                      ('back2',True):('dorsal',True),('atr1',True):('dorsal',True),
                                      ('high3', False): ('dorsal', True), ('low3', False): ('dorsal', True),
                                      ('front3', False): ('dorsal', True), ('back3', False): ('dorsal', True),
                                      ('atr2', False): ('dorsal', True),}


        self.show()

    def are_they_all_there(self, to_split):
        elements = re.split(',', to_split)
        checker = True
        for element in elements:
            if element in inventories[self.parent.choose_box.currentText()]["All Phonemes"]:
                pass
            elif element == '':
                pass
            else:
                checker = False
        return checker

    def save_changes(self):
        new_inventory = []
        the_input = self.entry_box.toPlainText()
        
        the_input = re.sub(' ', '', the_input)
        if the_input == '':
            hey_man = QtWidgets.QMessageBox.warning(self, "Input Missing!!!",
                                                    "You Need to Put in Phonemes.",
                                                    QMessageBox.Ok)
            return False
        elif self.are_they_all_there(the_input) == False:
            hey_man = QtWidgets.QMessageBox.warning(self, "Unacceptable Phoneme",
                                                    "One of the phonemes in the provided list does not exist.")
            return False
        changed_phonemes = the_input.split(',')

        check_input_again = re.sub(' ', '', the_input)
        check_input_again = re.sub(',', '', the_input)
        if check_input_again == '':
            hey_man = QtWidgets.QMessageBox.warning(self, "Input Missing!!!",
                                                    "You Need to Put in Phonemes.",
                                                    QMessageBox.Ok)
            return False
         #for whatever reason, the function threw a hissy fit because
         #there was an extra nothing character at the end, so that's why I need this next line here.

        changed_phonemes = [a for a in changed_phonemes if a != '']
        #
        # Now that We got the phonemes, let's take a look at the changed features

        attribute_map = {}
        was_there_a_change = False
        for key in self.value_map:
            if self.value_map[key].text() != "Null":
                was_there_a_change = True
                attribute_map[key] = self.value_map[key].text()

        if was_there_a_change == False:
            return None
        else:
            
            
            ## this kind of corrects stuff so it all runs smoother

            for key in attribute_map:
                if attribute_map[key] == "To Null":
                    attribute_map[key] = None
                elif attribute_map[key] == "True":
                    attribute_map[key] = True
                elif attribute_map[key]== "False":
                    attribute_map[key] = False



        ### Now we need to make a nwe version of each phoneme that is changed according to the defined parameters.


        to_be_remade_phonemes = []
        unremade_phonemes = []

        for extant_phoneme in dictionish[self.parent.choose_box.currentText()]:
            name = ""
            for extant_attribute in extant_phoneme:
                if extant_attribute[0] == 'name':
                    name = extant_attribute[1]
            
            if name in changed_phonemes:
                to_be_remade_phonemes.append(extant_phoneme)
            elif name not in changed_phonemes:
                unremade_phonemes.append(extant_phoneme)

        remakes =[]
        
        for phoneme_to_be_changed in to_be_remade_phonemes:
            
            remake = []
            for attribute in phoneme_to_be_changed:
                
                if attribute[0] in attribute_map:
                    
                    
                    new_attr = (attribute[0],attribute_map[attribute[0]])
                    
                    remake.append(new_attr)
                else:
                    remake.append(attribute)
            remake = tuple(remake)
            remakes.append(remake)


        
        final_list = remakes + unremade_phonemes

        dictionish[self.chosenInventory] = final_list
        reset_phoneme_map()
        inventory_update.set_off()
        hey_man = QMessageBox.warning(self,"Changes Saved","You have successfully altered the phonemes",QMessageBox.Ok)
        
        
        self.parent.close()
        self.close()


class save_options(QtWidgets.QDialog):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent

        self.pop_up = QtWidgets.QMessageBox()
        self.pop_up.setWindowTitle("Redundant Phonemes")
        self.pop_up.setText("Some of the phonemes are redundant. Would  you like to overwrite the new ones in, import them side-by-side with an altered name, or skip them?")
        self.pop_up.addButton(QtWidgets.QPushButton("Overwrite"),QtWidgets.QMessageBox.YesRole)
        self.pop_up.addButton(QtWidgets.QPushButton("Import Side by Side"),QtWidgets.QMessageBox.YesRole)
        self.pop_up.addButton(QtWidgets.QPushButton("Skip"), QtWidgets.QMessageBox.NoRole)
        self.pop_up.addButton(QtWidgets.QPushButton("Cancel"), QtWidgets.QMessageBox.NoRole)
        self.pop_up.exec_()
        

class data_pack_management(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle("Transfer Data")
        self.setWindowIcon(QtGui.QIcon('pictures/export.png'))
    def init_ui(self):
        self.granderHbox = QtWidgets.QHBoxLayout()
        self.grandVbox = QtWidgets.QVBoxLayout()


        self.picture_hbox = QtWidgets.QHBoxLayout()
        self.logo = QtGui.QPixmap('pictures/export2.png')
        self.logo = self.logo.scaled(200, 125, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.picture = QtWidgets.QLabel()
        self.picture.setPixmap(self.logo)
        self.picture.setFixedWidth(250)
        self.picture_hbox.addStretch(1)
        self.picture_hbox.addWidget(self.picture)
        self.picture_hbox.addStretch(1)

        self.grandVbox.addLayout(self.picture_hbox)


        self.h_box1 = QtWidgets.QHBoxLayout()
        self.h_box1.addStretch()
        self.export_label = QtWidgets.QLabel("Export From")
        self.export_label.setFixedWidth(150)
        self.h_box1.addWidget(self.export_label)
        self.inventory_export_box = QComboBox()
        self.inventory_export_box.setFixedWidth(200)
        self.inventory_export_box.addItem("Null")
        self.h_box1.addWidget(self.inventory_export_box)
        self.h_box1.addStretch()

        self.h_box2 = QtWidgets.QHBoxLayout()
        self.h_box2.addStretch()

        self.language_label = QtWidgets.QLabel("Choose a Language (if any)")
        self.language_label.setFixedWidth(150)
        self.h_box2.addWidget(self.language_label)
        self.language_box = QComboBox()
        self.language_box.setFixedWidth(200)
        self.language_box.addItem("No Languages or Phonemes")
        self.language_box.addItem("All Languages/Inventories")
        self.h_box2.addWidget(self.language_box)
        self.h_box2.addStretch()
        self.data_pack_name_label = QtWidgets.QLabel("Choose a Name for the data pack (no spaces)")
        self.datapack_name_line = QtWidgets.QLineEdit()



        for key in feature_set_map:
            self.inventory_export_box.addItem(key)
        self.inventory_export_box.activated[str].connect(self.update_language_list)
        self.languages = 0

        self.export_feature_groups = QCheckBox()
        self.export_feature_groups.setText("Export Feature Groups Too")
        self.export_entailments = QCheckBox()
        self.export_entailments.setText("Export Entailments Too")
        #self.import_languages = QCheckBox()
        #self.import_languages.setText("Import Language Inventories")

        self.transfer_btn = QtWidgets.QPushButton()
        self.transfer_btn.setText("Export")


        self.grandVbox.addLayout(self.h_box1)
        self.grandVbox.addLayout(self.h_box2)
        self.grandVbox.addWidget(self.data_pack_name_label)
        self.grandVbox.addWidget(self.datapack_name_line)
        self.grandVbox.addWidget(self.export_feature_groups)
        self.grandVbox.addWidget(self.export_entailments)
        #self.grandVbox.addWidget(self.import_languages)
        self.grandVbox.addWidget(self.transfer_btn)

        self.granderHbox.addLayout(self.grandVbox)

        """
        self.other_grandVbox = QtWidgets.QVBoxLayout()
        self.import_label = QtWidgets.QLabel("Import Datapack")
        self.import_line = QtWidgets.QLineEdit()
        self.import_btn = QtWidgets.QPushButton("Import")

        self.other_grandVbox.addWidget(self.import_label)
        self.other_grandVbox.addWidget(self.import_line)
        self.other_grandVbox.addWidget(self.import_btn)

        self.granderHbox.addLayout(self.other_grandVbox)
        """
        self.setLayout(self.granderHbox)
        self.transfer_btn.clicked.connect(self.save_data_pack)
        #self.import_btn.clicked.connect(self.import_data_pack)
        self.show()

    def update_language_list(self):
        for number in range(self.languages):
            self.language_box.removeItem(1)
            self.languages -= 1
        for language in inventories[self.inventory_export_box.currentText()]:
            self.language_box.addItem(language)
            self.languages += 1

    # thanks Keith the Coder from youtube!
    def createFolder(self,directory):
        
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
                
        except OSError:
            print ("Sorry, This didn't work out with the %s directory :(" %directory)

    def checkPath(self,directory):
        if os.path.exists(directory):
            return True
        else:
            return False

    def save_data_pack(self):

        print(self.checkPath("basic_pack"))
        print(self.checkPath("well that wasn't"))
        if self.datapack_name_line.text() == "":
            hey_man = QMessageBox.warning(self,"Name Needed","You need to give your Datapack a name",QMessageBox.Ok)
            return None
        elif self.checkPath(self.datapack_name_line.text()) == True:
            hey_man = QMessageBox.warning(self,"Path Taken","Choose a Different Name. Something in your Directory Already Has this Name")
            return None

        directory ="./"
        directory += self.datapack_name_line.text()
        directory += "/"

        self.createFolder(directory)

        # Ok, the data that we save needs to depend on what boxes were checked and how the boxes were filled out.

        # first, the feature set.
        feature_set_map_entry = feature_set_map[self.inventory_export_box.currentText()]
        with open(directory+"feature_set_map_entry", "wb") as f:
            pickle.dump(feature_set_map_entry, f)

        if self.language_box.currentText() == "No Languages or Phonemes":
            pass
        elif self.language_box.currentText() == "All Languages/Inventories":
            dictionish_entry = dictionish[self.inventory_export_box.currentText()]
            with open(directory + "dictionish_entry", "wb") as f:
                pickle.dump(dictionish_entry, f)
            inventories_entry =inventories[self.inventory_export_box.currentText()]
            with open(directory + "inventories_entry", "wb") as f:
                pickle.dump(inventories_entry, f)
        else:

            inventories_entry = {}
            inventories_entry["All Phonemes"] = inventories[self.inventory_export_box.currentText()][self.language_box.currentText()]
            inventories_entry[self.language_box.currentText()] = inventories[self.inventory_export_box.currentText()][self.language_box.currentText()]
            with open(directory + "inventories_entry", "wb") as f:
                pickle.dump(inventories_entry, f)

            # the dictionish entry can only consist of phonemes in the chosen language.

            dictionish_entry = []
            for candidate in dictionish[self.inventory_export_box.currentText()]:
                for attribute in candidate:
                    if attribute[0] == "name" and attribute[1] in inventories_entry["All Phonemes"]:
                        dictionish_entry.append(candidate)
            with open(directory + "dictionish_entry", "wb") as f:
                pickle.dump(dictionish_entry, f)

        # Now to see if the other bits of data get saved too.
        technical_map_entry = {"keyCategories":{},"Entailments":{}}

        if self.export_feature_groups.isChecked() == True:
            technical_map_entry["keyCategories"] = technical_map[self.inventory_export_box.currentText()]["keyCategories"]
            
        if self.export_entailments.isChecked() == True:
            technical_map_entry["Entailments"] = technical_map[self.inventory_export_box.currentText()]["Entailments"]

        with open(directory + "technical_map_entry", "wb") as f:
            pickle.dump(technical_map_entry, f)

        hey_man_icon_giver_2 = QMainWindow()
        hey_man_icon_giver_2.setWindowIcon(QtGui.QIcon("pictures/save"))
        hey_man_icon_giver_2.hide()
        print(type(hey_man_icon_giver_2))
        hey_man_2 = QMessageBox.information(hey_man_icon_giver_2, "Success!",
                                            "Successfully Saved the Datapack named %s"%(self.datapack_name_line.text()))
    def import_data_pack(self):
        directory = self.import_line.text()
        directory+= "/"
        pickle_in = open(directory+"feature_set_map_entry", "rb")
        feature_set_candidate = pickle.load(pickle_in)
        pickle_in.close()
        pickle_in = open(directory+"dictionish_entry", "rb")
        dictionish_candidate = pickle.load(pickle_in)
        pickle_in.close()
        pickle_in = open(directory+"inventories_entry", "rb")
        inventories_candidate = pickle.load(pickle_in)
        pickle_in.close()
        pickle_in = open(directory+"technical_map_entry", "rb")
        technical_map_candidate = pickle.load(pickle_in)
        pickle_in.close()

        ## what if there are two equal sets? lol
        totally_new = True

        for featureset in feature_set_map:
            pass

        for featureset in feature_set_map:
            totally_new = True
            if are_the_lists_the_same(feature_set_map[featureset],feature_set_candidate) == True:
                
                totally_new = False
                hey_man = import_options(self,featureset)
                if hey_man.pop_up.clickedButton().text() == "Overwrite":
                    feature_set_map[featureset] = feature_set_candidate
                    dictionish[featureset] = dictionish_candidate
                    inventories[featureset] = inventories_candidate
                    technical_map[featureset] = technical_map_candidate
                elif hey_man.pop_up.clickedButton().text() == "Combine":
                    # first, I'll handle dictionish
                    newcomers = []
                    for candidate in dictionish_candidate:
                        for attribute in candidate:
                            if attribute[0] == "name" and attribute[1] not in inventories[featureset]["All Phonemes"]:
                                newcomers.append(candidate)

                    new_dictionish = newcomers + dictionish[featureset]
                    dictionish[featureset] = new_dictionish
                    # handlign inventories
                    for key in inventories_candidate:
                        if key != "All Phonemes":
                            inventories[key] = inventories_candidate[key]

                    # handling featuregroups
                    if bool(technical_map_candidate["keyCategories"]) != False:
                        hey_man = QMessageBox.question(self,"Import Feature Groups?","Would you like to take in this data pack's Feature Groups by Overwriting what you already have?",
                                                       QMessageBox.Yes|QMessageBox.No)
                        if hey_man == QMessageBox.Yes:
                            technical_map[featureset]["keyCategories"] = technical_map_candidate["keyCategories"]
                        else:
                            pass
                    # handling entailments

                    if bool(technical_map_candidate["keyCategories"]) != False:
                        hey_man = QMessageBox.question(self,"Import Entailments?","Would you like to take in this data pack's Entailments by Overwriting what you already have?",
                                                       QMessageBox.Yes|QMessageBox.No)
                        if hey_man == QMessageBox.Yes:
                            technical_map[featureset]["Entailments"] = technical_map_candidate["Entailments"]
                else:
                    return None

            elif totally_new == True:
                featureset_name = ""
                name,dialogue = QInputDialog(self,'Select a Name',"Pick a name for the new featureset.")
                if dialogue == True:
                    featureset_name = str(name)
                else:
                    return None

                feature_set_map[featureset_name] = feature_set_candidate
                technical_map[featureset_name] = [technical_map_candidate]
                inventories[featureset_name] = inventories_candidate
                dictionish[featureset_name] = dictionish_candidate
            inventory_update.set_off()
            reset_phoneme_map()
            hey_man = QMessageBox.information(self,"Data Import complete!","Everything has been successfully imported.",QMessageBox.Ok)

def are_the_lists_the_same(list1,list2):
    list1_contained_in_list_2 = True
    for element in list1:
        if element not in list2:
            list1_contained_in_list_2 = False
    list2_contained_in_list_1 = True
    for other_element in list2:
        if other_element not in list1:
            list2_contained_in_list_1 = False

    if list2_contained_in_list_1 == False or list1_contained_in_list_2 == False:
        return False
    else:
        return True

class import_options(QtWidgets.QDialog):
    def __init__(self,parent,lang):
        super().__init__()
        self.parent = parent

        self.pop_up = QtWidgets.QMessageBox()
        self.pop_up.setWindowTitle("Overwrite Featureset?")
        self.pop_up.setText("The featureset you are trying to import is equal to the featureset %s that you already have. Would you like to have the new featureset Overwrite and replace, or would you like to combine them?"%(lang))
        self.pop_up.addButton(QtWidgets.QPushButton("Overwrite"),QtWidgets.QMessageBox.YesRole)
        self.pop_up.addButton(QtWidgets.QPushButton("Combine"),QtWidgets.QMessageBox.YesRole)
        self.pop_up.addButton(QtWidgets.QPushButton("Cancel"), QtWidgets.QMessageBox.NoRole)
        self.pop_up.exec_()
        

def import_file_dialog(window_to_update = None):

    tkSearch = Tk()
    tkSearch.withdraw()
    tkSearch.fileName = filedialog.askdirectory()

    directory = tkSearch.fileName



    if os.path.isfile(directory + "/feature_set_map_entry") and os.path.isfile(directory + "/dictionish_entry") and os.path.isfile(directory + "/inventories_entry") and os.path.isfile(directory + "/technical_map_entry"):



        #directory = self.import_line.text()
        directory += "/"
        pickle_in = open(directory + "/feature_set_map_entry", "rb")
        feature_set_candidate = pickle.load(pickle_in)
        pickle_in.close()
        pickle_in = open(directory + "/dictionish_entry", "rb")
        dictionish_candidate = pickle.load(pickle_in)
        pickle_in.close()
        pickle_in = open(directory + "/inventories_entry", "rb")
        inventories_candidate = pickle.load(pickle_in)
        pickle_in.close()
        pickle_in = open(directory + "/technical_map_entry", "rb")
        technical_map_candidate = pickle.load(pickle_in)
        pickle_in.close()

        ## what if there are two equal sets? lol
        totally_new = True

        for featureset in feature_set_map:
            pass

        for featureset in feature_set_map:
            pass

            if are_the_lists_the_same(feature_set_map[featureset], feature_set_candidate) == True:
                
                totally_new = False
                hey_man = import_options(None, featureset)
                if hey_man.pop_up.clickedButton().text() == "Overwrite":
                    feature_set_map[featureset] = feature_set_candidate
                    dictionish[featureset] = dictionish_candidate
                    inventories[featureset] = inventories_candidate
                    technical_map[featureset] = technical_map_candidate
                elif hey_man.pop_up.clickedButton().text() == "Combine":
                    # first, I'll handle dictionish
                    newcomers = []
                    for candidate in dictionish_candidate:
                        for attribute in candidate:
                            if attribute[0] == "name" and attribute[1] not in inventories[featureset]["All Phonemes"]:
                                newcomers.append(candidate)

                    new_dictionish = newcomers + dictionish[featureset]
                    dictionish[featureset] = new_dictionish
                    # handlign inventories
                    for key in inventories_candidate:
                        if key != "All Phonemes":
                            inventories[key] = inventories_candidate[key]

                    # handling featuregroups
                    if bool(technical_map_candidate["keyCategories"]) != False:
                        hey_man = QMessageBox.question(None, "Import Feature Groups?",
                                                       "Would you like to take in this data pack's Feature Groups by Overwriting what you already have?",
                                                       QMessageBox.Yes | QMessageBox.No)
                        if hey_man == QMessageBox.Yes:
                            technical_map[featureset]["keyCategories"] = technical_map_candidate["keyCategories"]
                        else:
                            pass
                    # handling entailments

                    if bool(technical_map_candidate["keyCategories"]) != False:
                        hey_man = QMessageBox.question(None, "Import Entailments?",
                                                       "Would you like to take in this data pack's Entailments by Overwriting what you already have?",
                                                       QMessageBox.Yes | QMessageBox.No)
                        if hey_man == QMessageBox.Yes:
                            technical_map[featureset]["Entailments"] = technical_map_candidate["Entailments"]
                        else:
                            pass
                else:
                    
                    return None

        
        if totally_new == True:
            
            featureset_name = ""

            hey_man_icon = QMainWindow()
            hey_man_icon.setWindowIcon(QtGui.QIcon('pictures/main logo.png'))
            hey_man_icon.hide()
            name, dialogue = QInputDialog.getText(hey_man_icon, 'Select a Name', "Pick a name for the new featureset.")
            if dialogue == True:
                hey_man_icon.close()
                featureset_name = str(name)
            else:
                hey_man_icon.close()
                return None
            
            feature_set_map[featureset_name] = feature_set_candidate
            technical_map[featureset_name] = technical_map_candidate
            inventories[featureset_name] = inventories_candidate
            dictionish[featureset_name] = dictionish_candidate
            
            
            
            
            

        inventory_update.set_off()

        reset_phoneme_map()
        hey_man_icon_giver = QMainWindow()
        hey_man_icon_giver.setWindowIcon(QtGui.QIcon('pictures/save.png'))
        hey_man_icon_giver.hide()
        hey_man = QMessageBox.information(hey_man_icon_giver, "Data Import complete!", "Everything has been successfully imported.",
                                          QMessageBox.Ok)
        hey_man_icon_giver.close()
        print(window_to_update)
        if window_to_update != None:

            window_to_update.update_inventory_list()
        else:
            pass
    elif directory == "":
        hey_man_icon_giver = QMainWindow()
        hey_man_icon_giver.setWindowIcon(QtGui.QIcon('pictures/error.png'))
        hey_man_icon_giver.hide()
        hey_man = QMessageBox.information(hey_man_icon_giver, "Import Canceled",
                                          "The import has been canceled.",
                                          QMessageBox.Ok)
        hey_man_icon_giver.close()
    else:
        hey_man_icon_giver = QMainWindow()
        hey_man_icon_giver.setWindowIcon(QtGui.QIcon('pictures/error.png'))
        hey_man_icon_giver.hide()
        hey_man = QMessageBox.information(hey_man_icon_giver, "Data Import Failed!", "The Folder you chose was somehow incomplete.",
                                          QMessageBox.Ok)
        hey_man_icon_giver.close()


    tkSearch.destroy()


def import_file_dialog_hardcoded_test_version():


    directory = "C:/Users/puistori/PycharmProjects/myStuff/chesire_mac"
    
    if os.path.isfile(directory + "/feature_set_map_entry") and os.path.isfile(
            directory + "/dictionish_entry") and os.path.isfile(directory + "/inventories_entry") and os.path.isfile(
            directory + "/technical_map_entry"):

        # directory = self.import_line.text()
        directory += "/"
        pickle_in = open(directory + "/feature_set_map_entry", "rb")
        feature_set_candidate = pickle.load(pickle_in)
        pickle_in.close()
        pickle_in = open(directory + "/dictionish_entry", "rb")
        dictionish_candidate = pickle.load(pickle_in)
        pickle_in.close()
        pickle_in = open(directory + "/inventories_entry", "rb")
        inventories_candidate = pickle.load(pickle_in)
        pickle_in.close()
        pickle_in = open(directory + "/technical_map_entry", "rb")
        technical_map_candidate = pickle.load(pickle_in)
        pickle_in.close()

        ## what if there are two equal sets? lol
        totally_new = True

        for featureset in feature_set_map:
            pass

        for featureset in feature_set_map:
            if are_the_lists_the_same(feature_set_map[featureset], feature_set_candidate) == True:
                
                totally_new = False

                if 1+1 ==4:
                    feature_set_map[featureset] = feature_set_candidate
                    dictionish[featureset] = dictionish_candidate
                    inventories[featureset] = inventories_candidate
                    technical_map[featureset] = technical_map_candidate
                elif 1+1 ==2:
                    # first, I'll handle dictionish
                    newcomers = []
                    for candidate in dictionish_candidate:
                        for attribute in candidate:
                            if attribute[0] == "name" and attribute[1] not in inventories[featureset]["All Phonemes"]:
                                newcomers.append(candidate)

                    new_dictionish = newcomers + dictionish[featureset]
                    dictionish[featureset] = new_dictionish
                    # handlign inventories
                    for key in inventories_candidate:
                        if key != "All Phonemes":
                            inventories[key] = inventories_candidate[key]

                    # handling featuregroups
                    if bool(technical_map_candidate["keyCategories"]) != False:
                        if 1+1==2:
                            technical_map[featureset]["keyCategories"] = technical_map_candidate["keyCategories"]
                        else:
                            pass
                    # handling entailments

                    if bool(technical_map_candidate["keyCategories"]) != False:

                        if 1+1 ==2:
                            technical_map[featureset]["Entailments"] = technical_map_candidate["Entailments"]
                        else:
                            pass
                else:
                    
                    return None

        if totally_new == True:
            featureset_name = ""
            name, dialogue = QInputDialog.getText(None,'Select a Name', "Pick a name for the new featureset.")
            if dialogue == True:
                featureset_name = str(name)
            else:
                return None
            feature_set_map[featureset_name] = feature_set_candidate
            technical_map[featureset_name] = technical_map_candidate
            
            
            
            inventories[featureset_name] = inventories_candidate
            dictionish[featureset_name] = dictionish_candidate
        inventory_update.set_off()

        reset_phoneme_map()
        
        pass
    else:
        pass

class trash_can(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super().__init__()
        self.parent = parent
        self.init_ui()
    def init_ui(self):

        self.grandHbox = QtWidgets.QHBoxLayout()


        self.logo = QtGui.QPixmap('pictures/garbage can.png')
        self.logo = self.logo.scaled(200, 200, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.picture = QtWidgets.QLabel()
        self.picture.setPixmap(self.logo)
        self.picture.setFixedWidth(200)


        self.delete_phoneme_frame = QtWidgets.QFrame()
        self.delete_phoneme_frame.setStyleSheet("background-color: %s;"%light_brown.name())
        self.delete_phoneme_vbox = QtWidgets.QVBoxLayout(self.delete_phoneme_frame)

        self.delete_phoneme_label_hbox = QtWidgets.QHBoxLayout()
        self.delete_phoneme_label = QtWidgets.QLabel("Delete a Phoneme")
        self.delete_phoneme_label.setStyleSheet("background-color: %s;"%light_gray.name())
        self.delete_phoneme_label_hbox.addStretch(1)
        self.delete_phoneme_label_hbox.addWidget(self.delete_phoneme_label)
        self.delete_phoneme_label_hbox.addStretch(1)

        self.delete_phoneme_inventory_hbox = QtWidgets.QHBoxLayout()
        self.delete_phoneme_inventory_selection_label = QtWidgets.QLabel("Select a Feature-set: ")
        self.delete_phoneme_inventory_selection_box = QtWidgets.QComboBox()
        self.delete_phoneme_inventory_selection_box.addItem("Null")
        self.delete_phoneme_inventory_selection_box.setStyleSheet("background-color: white;")
        self.delete_phoneme_inventory_selection_box.setFixedWidth(90)
        self.delete_phoneme_inventory_hbox.addWidget(self.delete_phoneme_inventory_selection_label)
        self.delete_phoneme_inventory_hbox.addWidget(self.delete_phoneme_inventory_selection_box)

        self.delete_phoneme_language_hbox = QtWidgets.QHBoxLayout()
        self.delete_phoneme_language_selection_label = QtWidgets.QLabel("Select a Phoneme Inventory: ")
        self.delete_phoneme_language_selection_box = QtWidgets.QComboBox()
        self.delete_phoneme_language_selection_box.addItem("Null")
        self.delete_phoneme_language_selection_box.setStyleSheet("background-color: white;")
        self.delete_phoneme_language_selection_box.setFixedWidth(90)
        self.delete_phoneme_language_hbox.addWidget(self.delete_phoneme_language_selection_label)
        self.delete_phoneme_language_hbox.addWidget(self.delete_phoneme_language_selection_box)

        self.phoneme_delete_line_hbox = QtWidgets.QHBoxLayout()
        self.phoneme_delete_line_edit = QtWidgets.QLineEdit()
        self.phoneme_delete_line_edit.setStyleSheet("background-color: white;")
        self.phoneme_delete_line_assistive_click = QtWidgets.QPushButton("Assistive Click")
        self.phoneme_delete_line_assistive_click.setStyleSheet("background-color: %s;"%light_gray.name())
        self.phoneme_delete_line_hbox.addWidget(self.phoneme_delete_line_edit)
        self.phoneme_delete_line_hbox.addWidget(self.phoneme_delete_line_assistive_click)

        self.phoneme_delete_button = QtWidgets.QPushButton("Delete Phoneme")
        self.phoneme_delete_button.setStyleSheet("background-color: %s;"%light_gray.name())

        self.delete_phoneme_vbox.addLayout(self.delete_phoneme_label_hbox)
        self.delete_phoneme_vbox.addLayout(self.delete_phoneme_inventory_hbox)
        self.delete_phoneme_vbox.addLayout(self.delete_phoneme_language_hbox)
        self.delete_phoneme_vbox.addLayout(self.phoneme_delete_line_hbox)
        self.delete_phoneme_vbox.addWidget(self.phoneme_delete_button)
        self.delete_phoneme_vbox.addStretch(1)

        self.delete_phoneme_inventory_selection_box.activated.connect(partial(self.update_language_list,self.delete_phoneme_language_selection_box))
        self.phoneme_delete_line_assistive_click.clicked.connect(self.show_assistive_click)
        self.phoneme_delete_line_edit.textChanged[str].connect(
            partial(self.remove_comma, self.phoneme_delete_line_edit))
        self.phoneme_delete_button.clicked.connect(self.delete_phoneme_function)

        # connect


        self.delete_inventory_frame = QtWidgets.QFrame()
        self.delete_inventory_frame.setStyleSheet("background-color: %s;"%light_red.name())
        self.delete_inventory_vbox = QtWidgets.QVBoxLayout(self.delete_inventory_frame)

        self.delete_inventory_label_hbox = QtWidgets.QHBoxLayout()
        self.delete_inventory_label = QtWidgets.QLabel("Delete a Phoneme Inventory")
        self.delete_inventory_label.setStyleSheet("background-color: %s;"%light_gray.name())
        self.delete_inventory_label_hbox.addStretch(1)
        self.delete_inventory_label_hbox.addWidget(self.delete_inventory_label)
        self.delete_inventory_label_hbox.addStretch(1)


        self.delete_inventory_inventory_hbox = QtWidgets.QHBoxLayout()
        self.delete_inventory_inventory_selection_label = QtWidgets.QLabel("Select a Feature-set: ")
        self.delete_inventory_inventory_selection_box = QtWidgets.QComboBox()
        self.delete_inventory_inventory_selection_box.setStyleSheet("background-color: white;")
        self.delete_inventory_inventory_selection_box.addItem("Null")
        self.delete_inventory_inventory_selection_box.setFixedWidth(90)
        self.delete_inventory_inventory_hbox.addWidget(self.delete_inventory_inventory_selection_label)
        self.delete_inventory_inventory_hbox.addWidget(self.delete_inventory_inventory_selection_box)

        self.delete_inventory_language_hbox = QtWidgets.QHBoxLayout()
        self.delete_inventory_language_selection_label = QtWidgets.QLabel("Select a Phoneme Inventory: ")
        self.delete_inventory_language_selection_box = QtWidgets.QComboBox()
        self.delete_inventory_language_selection_box.setStyleSheet("background-color: white;")
        self.delete_inventory_language_selection_box.addItem("Null")
        self.delete_inventory_language_selection_box.setFixedWidth(90)
        self.delete_inventory_language_hbox.addWidget(self.delete_inventory_language_selection_label)
        self.delete_inventory_language_hbox.addWidget(self.delete_inventory_language_selection_box)

        self.inventory_delete_button = QtWidgets.QPushButton("Delete Phoneme Inventory")
        self.inventory_delete_button.setStyleSheet("background-color: %s;"%light_gray.name())

        self.delete_inventory_vbox.addLayout(self.delete_inventory_label_hbox)
        self.delete_inventory_vbox.addStretch(1)
        self.delete_inventory_vbox.addLayout(self.delete_inventory_inventory_hbox)
        self.delete_inventory_vbox.addLayout(self.delete_inventory_language_hbox)
        self.delete_inventory_vbox.addWidget(self.inventory_delete_button)
        self.delete_inventory_vbox.addStretch(2)

        self.delete_inventory_inventory_selection_box.activated.connect(partial(self.update_language_list,self.delete_inventory_language_selection_box))
        self.inventory_delete_button.clicked.connect(self.delete_inventory_function)
        # connect

        self.delete_feature_set_frame = QtWidgets.QFrame()
        self.delete_feature_set_frame.setStyleSheet("background-color: %s;" % light_orange.name())
        self.delete_feature_set_vbox = QtWidgets.QVBoxLayout(self.delete_feature_set_frame)

        self.delete_feature_set_label_hbox = QtWidgets.QHBoxLayout()
        self.delete_feature_set_label = QtWidgets.QLabel("Delete a Phoneme Inventory")
        self.delete_feature_set_label.setStyleSheet("background-color: %s;"%light_gray.name())
        self.delete_feature_set_label_hbox.addStretch(1)
        self.delete_feature_set_label_hbox.addWidget(self.delete_feature_set_label)
        self.delete_feature_set_label_hbox.addStretch(1)

        self.delete_feature_set_inventory_hbox = QtWidgets.QHBoxLayout()
        self.delete_feature_set_inventory_selection_label = QtWidgets.QLabel("Select a Feature-set: ")
        self.delete_feature_set_inventory_selection_box = QtWidgets.QComboBox()
        self.delete_feature_set_inventory_selection_box.setStyleSheet("background-color: white;")
        self.delete_feature_set_inventory_selection_box.addItem("Null")
        self.delete_feature_set_inventory_selection_box.setFixedWidth(90)
        self.delete_feature_set_inventory_hbox.addWidget(self.delete_feature_set_inventory_selection_label)
        self.delete_feature_set_inventory_hbox.addWidget(self.delete_feature_set_inventory_selection_box)


        self.feature_set_delete_button = QtWidgets.QPushButton("Delete Feature-set")
        self.feature_set_delete_button.setStyleSheet("background-color: %s;"%light_gray.name())

        self.delete_feature_set_vbox.addLayout(self.delete_feature_set_label_hbox)
        self.delete_feature_set_vbox.addStretch(1)
        self.delete_feature_set_vbox.addLayout(self.delete_feature_set_inventory_hbox)
        self.delete_feature_set_vbox.addWidget(self.feature_set_delete_button)
        self.delete_feature_set_vbox.addStretch(1)

        self.feature_set_delete_button.clicked.connect(self.delete_feature_set_function)
        # connect


        # now slapping them all together :)

        self.grandHbox.addWidget(self.picture)
        self.grandHbox.addWidget(self.delete_phoneme_frame)
        self.grandHbox.addWidget(self.delete_inventory_frame)
        self.grandHbox.addWidget(self.delete_feature_set_frame)
        self.setLayout(self.grandHbox)

        self.setWindowTitle("Trash Can")
        self.setWindowIcon(QtGui.QIcon('pictures/garbage can'))

        self.inventory_count = 0
        self.phoneme_delete_language_count = 0
        self.inventory_delete_language_count = 0

        self.language_box_dictionary = {self.delete_phoneme_language_selection_box : [self.delete_phoneme_inventory_selection_box,self.phoneme_delete_language_count],
                                        self.delete_inventory_language_selection_box :[self.delete_inventory_inventory_selection_box,self.inventory_delete_language_count]}
        self.update_feature_set()

        self.show()


    def update_feature_set(self):
        combo_box_list = [self.delete_phoneme_inventory_selection_box,self.delete_inventory_inventory_selection_box,self.delete_feature_set_inventory_selection_box]

        for member in combo_box_list:
            for number in range(self.inventory_count):
                member.removeItem(1)
            for key in feature_set_map:
                member.addItem(key)

        new_inventory_count = 0
        for key in feature_set_map:
            new_inventory_count += 1

        self.inventory_count = new_inventory_count

    def update_language_list(self,target):

        list_all_phonemes = True
        if target == self.delete_inventory_language_selection_box:
            list_all_phonemes = False
        new_lang_count = 0
        current_feature_set = self.language_box_dictionary[target][0].currentText()
        language_count = self.language_box_dictionary[target][1]

        if language_count > 0:
            for number in range(language_count):
                target.removeItem(1)

        if current_feature_set == "Null":
            pass

        else:
            for key in inventories[current_feature_set]:
                if key == "All Phonemes" and list_all_phonemes == False:
                    pass
                else:
                    target.addItem(key)
                    new_lang_count +=1
        self.language_box_dictionary[target][1] = new_lang_count

    def show_assistive_click(self):
        FS = self.delete_phoneme_inventory_selection_box.currentText()
        LNG = self.delete_phoneme_language_selection_box.currentText()
        if FS == "Null" or LNG == "Null":
            hey_man_icon_giver = QMainWindow()
            hey_man_icon_giver.setWindowIcon(QtGui.QIcon("pictures/aviso"))
            hey_man_icon_giver.hide()
            hey_man = QMessageBox.warning(hey_man_icon_giver,"Select Inventories","Select a Feature-set and a Phoneme Inventory First.")
            hey_man_icon_giver.close()
        else:
            self.assistive_click =assistive_click(self,self.phoneme_delete_line_edit,FS,LNG)


    def delete_phoneme_function(self):
        print("Prelength")
        poistettava_foneemi = self.phoneme_delete_line_edit.text()
        FS = self.delete_phoneme_inventory_selection_box.currentText()
        print(len(dictionish[FS]))
        if FS == "Null":
            hey_man_icon_giver = QMainWindow()
            hey_man_icon_giver.setWindowIcon(QtGui.QIcon("pictures/aviso"))
            hey_man_icon_giver.hide()
            hey_man = QMessageBox.warning(hey_man_icon_giver,"Select Inventory","Select a Feature-set Inventory First.")
            hey_man_icon_giver.close()
        else:
            #this is finnish for "phoneme to be removed"
            hey_man = QMessageBox.question(self, "Are you Sure?",
                                           "Are You Sure You Wish to Delete the Phoneme [%s] in the %s Feature-set?" %(poistettava_foneemi,FS),
                                           QMessageBox.Yes | QMessageBox.No)
            if hey_man == QMessageBox.Yes:



                ## Delete from Dictionish
                old_dictionish_entry = dictionish[FS]
                print("yehhoo!")
                print(old_dictionish_entry)
                print(self.get_the_name(old_dictionish_entry[0]))
                new_dictionish_entry = [a for a in old_dictionish_entry if self.get_the_name(a) != poistettava_foneemi ]
                print("yehhoo!")
                dictionish[FS] = new_dictionish_entry

                ## delete from Inventories:

                for inventory in inventories[FS]:
                    new_inventory = [a for a in inventories[FS][inventory] if a != poistettava_foneemi]
                    inventories[FS][inventory] = new_inventory

                hey_man_icon_giver_2 = QMainWindow()
                hey_man_icon_giver_2.setWindowIcon(QtGui.QIcon("pictures/save"))
                hey_man_icon_giver_2.hide()
                print(type(poistettava_foneemi))
                print(type(FS))
                print(type(hey_man_icon_giver_2))
                hey_man_2 = QMessageBox.information(hey_man_icon_giver_2, "Success!","Successfully Deleted the Phoneme [%s] from the %s Feature-Set"%(poistettava_foneemi,FS))
                hey_man_icon_giver_2.close()
                print("now inventories")
                print(inventories[FS])
                print("afterlength")
                print(len(dictionish[FS]))
                reset_phoneme_map()
                inventory_update.set_off()

            else:
                pass

    def delete_inventory_function(self):


        FS = self.delete_inventory_inventory_selection_box.currentText()
        LNG = self.delete_inventory_language_selection_box.currentText()
        if FS == "Null" or LNG == "Null":
            hey_man_icon_giver = QMainWindow()
            hey_man_icon_giver.setWindowIcon(QtGui.QIcon("pictures/aviso"))
            hey_man_icon_giver.hide()
            hey_man = QMessageBox.warning(hey_man_icon_giver,"Select Inventories","Select a Feature-set and a Phoneme Inventory First.")
            hey_man_icon_giver.close()
        else:
            hey_man = QMessageBox.question(self, "Are you Sure?",
                                           "Are You Sure You Wish to Delete the %s Feature-set?" % FS,
                                           QMessageBox.Yes | QMessageBox.No)
            if hey_man == QMessageBox.Yes:
                inventories[FS].pop(LNG,None)
                hey_man_icon_giver = QMainWindow()
                hey_man_icon_giver.setWindowIcon(QtGui.QIcon("pictures/save"))
                hey_man_icon_giver.hide()
                hey_man = QMessageBox.information(hey_man_icon_giver, "Success!",
                                              "Successfully Deleted the %s Inventory from the %s Feature-Set"%(LNG,FS))
                hey_man_icon_giver.close()
                self.update_language_list(self.delete_inventory_language_selection_box)
                self.update_language_list(self.delete_phoneme_language_selection_box)

                reset_phoneme_map()
                inventory_update.set_off()
            else:
                pass

    def delete_feature_set_function(self):
        FS = self.delete_feature_set_inventory_selection_box.currentText()
        if FS == "Null":
            hey_man_icon_giver = QMainWindow()
            hey_man_icon_giver.setWindowIcon(QtGui.QIcon("pictures/aviso"))
            hey_man_icon_giver.hide()
            hey_man = QMessageBox.warning(hey_man_icon_giver,"Select Inventory","Select a Feature-set Inventory First.")
            hey_man_icon_giver.close()
        else:
            hey_man = QMessageBox.question(self,"Are you Sure?","Are You Sure You Wish to Delete the %s Feature-set?"%FS,QMessageBox.Yes|QMessageBox.No)
            if hey_man == QMessageBox.Yes:
                dictionish.pop(FS,None)
                technical_map.pop(FS,None)
                inventories.pop(FS,None)
                feature_set_map.pop(FS,None)
                hey_man_icon_giver = QMainWindow()
                hey_man_icon_giver.setWindowIcon(QtGui.QIcon("pictures/save"))
                hey_man_icon_giver.hide()
                hey_man = QMessageBox.information(hey_man_icon_giver, "Success!",
                                                  "Successfully Deleted the %s Feature-Set" % (FS))
                hey_man_icon_giver.close()
                self.update_feature_set()
                self.parent.executive_window.update_inventory_list()
                self.parent.executive_window.update_language_list()

                reset_phoneme_map()
                inventory_update.set_off()

            else:
                pass

    def remove_comma(self,target):
        target.setText(re.sub(",","",target.text()))

    def get_the_name(self,tuple_of_choice):
        name = ""
        for subtuple in tuple_of_choice:
            print("checkin")
            if subtuple[0] == "name":
                name = subtuple[1]
                return name
        return None

app = QtWidgets.QApplication(sys.argv)

main_window = the_main_window()

sys.exit(app.exec_())



### Version 6 represents (most of ) the work i have done since giving my first copy of this stuff over to bakovic this summer.
### Version 8 represents pretty much all of it put together (with the trashcan added). I did a lot of work with adding icons and symbols and artwork and stuff on version 7.





### thank you this person!

# https://eli.thegreenplace.net/2011/04/25/passing-extra-arguments-to-pyqt-slot
# https://stackoverflow.com/questions/5899826/pyqt-how-to-remove-a-widget?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

# tuples to list: https://stackoverflow.com/questions/12836128/convert-list-to-tuple-in-python

# deleting dictionary keys: https://stackoverflow.com/questions/11277432/how-to-remove-a-key-from-a-python-dictionary

# buildFeatureSet - make it so you can't add redundant features?

# https://stackoverflow.com/questions/337688/dynamic-keyword-arguments-in-python

# add entailments and sound groups. That would probably work best with layering windows over the others.

## column width   https://stackoverflow.com/questions/19815061/pyside-set-width-of-qvboxlayout