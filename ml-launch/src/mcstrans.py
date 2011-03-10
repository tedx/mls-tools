#!/usr/bin/python -E
import sys, re
from operator import itemgetter
from odict import OrderedDict
#from constraint import *

lineno = 0
domain = None
group = None
baseClassification = None
domains = OrderedDict()
sensitivityConstraints = []
categoryConstraints = []

def containsAny(str, set):
    for c in set:
        if c in str: return 1;
    return 0;


def containsAll(str, set):
    for c in set:
        if c not in str: return 0;
    return 1;

class Codeword:
    def __init__(self, word, comment):
        self.word = word
        self.comment = comment
        self.used = False

class BaseClassification:

    def __init__(self, name):
        self.name = name
        self.sensitivities = OrderedDict()

    def addSensitivity(self, sensitivity, level):
        if self.sensitivities.has_key(sensitivity) == 0:
            self.sensitivities[sensitivity] = level

    def findSensitivityByName(self, sensitivity):
        for k, v in self.sensitivities.iteritems():
#            print k,v
            if v == sensitivity:
                return v, k
        return None
        
    def __str__(self):
        str = ""
        str = str + "Name: %s\n" % (self.name)
        str = str + "Sensitivities:\n"
        for key in self.sensitivities.keys():
            str = str + "%s %s\n" % (key, self.sensitivities[key])
        return str

class Group:

    def __init__(self, name):
        self.name = name
        self.wordDict = OrderedDict()
        self.whitespace = ""
        self.join = ""
        self.default = ""
        self.prefixes = []
        self.suffixes = []

    def __str__(self):
        str = ""
        str = str + "\nName: %s\n" % (self.name)
        str = str + "Whitespace: %s\n" % (self.whitespace)
        str = str + "Join: %s\n" % (self.join)
        str = str + "Default: %s\n" % (self.default)
        str = str + "Prefixes: %s\n" % (self.prefixes)
        str = str + "Suffixes: %s\n" % (self.suffixes)
        str = str + "Words:\n"
        for key in self.wordDict.keys():
            str = str + "%s %s\n" % (key, self.wordDict[key])
        return str

    def set_used_codeword(self, codeword):
        self.wordDict[codeword].used = True

    def count_used_codewords(self):
        count = 0
        for codeword in self.wordDict.values():
            if codeword.used:
                count += 1
        return count

    def get_used_codeword(self):
        def make_iter(self=self):
            for codeword in self.wordDict.values():
                if codeword.used:
                    yield codeword

        return make_iter()

    def get_unused_codeword(self):
        def make_iter(self=self):
            for codeword in self.wordDict.values():
                if not codeword.used:
                    yield codeword

        return make_iter()
        
class Domain:

    def __init__(self, name):
        self.name = name
        self.sensitivities = OrderedDict()
        self.baseClassifications = OrderedDict()
        self.rawToTrans = OrderedDict()
        self.transToRaw = OrderedDict()
        self.groups = OrderedDict()

    def addSensitivity(self, sensitivity, level):
        if self.sensitivities.has_key(sensitivity) == 0:
            self.sensitivities[sensitivity] = level

    def findSensitivityByName(self, sensitivity):
        for k, v in self.sensitivities.iteritems():
#            print k,v
            if v == sensitivity:
                return sensitivity
        return None
        

    def addGroup(self, groupName):
        group = Group(groupName)
        self.groups[groupName] = group
        return group

    def addBaseClassification(self, bcName):
        baseClassification = BaseClassification(bcName)
        self.baseClassifications[bcName] = baseClassification
        return baseClassification

    def str(self):
        str = ""
        str = str + "Domain name: %s\n" % (self.name)
        str = str + "Sensitivities:"
        for key in self.sensitivities.keys():
            str = str + "%s %s\n" % (key, self.sensitivities[key])
        str = str + "Base classifications:\n"
        for key in self.baseClassifications.keys():
            str = str + str(self.baseClassifications[key])
        str = str + "Groups:\n"
        for key in self.groups.keys():
            str = str + str(self.groups[key])
#        str = str + "Raw to translated:"
#        for key in self.rawToTrans.keys():
#            str = str + "%s %s" % (key, self.rawToTrans[key])
#        str = str + "Translated to raw:"
#        for key in self.transToRaw.keys():
#            str = str + "%s %s" % (key, self.transToRaw[key])
        return str

def process_file(fileName, debug):
    if debug:
        print("Process %s" % fileName)
    f=open(fileName, 'r')
    for line in f:
        process_line(line, debug)
    f.close()

# (IMHO) the simplest approach:
def sortDictByValues(d):
    di = sorted(d.iteritems(), key=itemgetter(1), reverse=False)
#    for key in d1.keys():
#        print "%s %s" % (key, d1[key])
#    for k, g in groupby(di, key=itemgetter(1)):
#        print k, map(itemgetter(0), g)    

    return di

# Process line from translation file. 
#   Remove white space and set raw do data before the "=" and tok to data after it
#   Modifies the data pointed to by the buffer parameter


def process_line(buffer, debug):
    global lineno, domain, baseClassification, group

    lineno = lineno + 1
    buffer.strip()
    buffer = buffer.rstrip('\n')
    if buffer.startswith('#'):
        return
    
    if buffer == "":
        return

    if debug:
        print "%d: %s" % (lineno, buffer)

    comment = None
    nvCommentList = buffer.split("#")
    if debug:
        print nvCommentList
    if len(nvCommentList) > 1:
        comment = nvCommentList[1]

    buffer = nvCommentList[0].rstrip(' \t')
    
    if containsAny(buffer, '>!'):
        if debug:
            print "constraint", buffer
#        if buffer.startswith('s'):
#            sensitivityConstraint = SensitivityConstraint(buffer, debug)
#            sensitivityConstraints.append(sensitivityConstraint)
#        else:
#            categoryConstraint = CategoryConstraint(buffer, debug)
#            categoryConstraints.append(categoryConstraint)
    else:
        nameValueList = buffer.split("=")
        if len(nameValueList) < 2:
            return

        if nameValueList[0] == "Domain":
            if debug:
                print "Add domain %s\n" % ( nameValueList[1])
            domain = Domain(nameValueList[1])
            domains[nameValueList[1]] = domain
            group = None
            return 0

        if domain == None:
            domain = Domain("Default")
            domains["Default"] = domain
            group = None

        if nameValueList[0] == "Include":
            process_file(nameValueList[1], debug)

        elif nameValueList[0] == "Base":
            if debug:
                print "Add baseClassification - %s\n" % (nameValueList[1])
            baseClassification = domain.addBaseClassification(nameValueList[1])
        elif nameValueList[0] == "ModifierGroup":
            if debug:
                print "Add group %s\n" % ( nameValueList[1])
            group = domain.addGroup(nameValueList[1])
            baseClassification = None

        elif nameValueList[0] == "Whitespace":
            group.whitespace = nameValueList[1]
        elif nameValueList[0] == "Join":
            group.join = nameValueList[1]
        elif nameValueList[0] == "Prefix":
            group.prefixes.append(nameValueList[1])
        elif nameValueList[0] == "Suffix":
            group.suffixes.append(nameValueList[1])
        elif nameValueList[0] == "Default":
            group.default = nameValueList[1]
        elif (group != None):
            if debug:
                print "Add word %s to %s\n" % (nameValueList[1], group.name)
            if group.wordDict.get(nameValueList[0]) == None:
                group.wordDict[nameValueList[0]] = Codeword(nameValueList[1], comment)

        else:
            if baseClassification != None:
                baseClassification.addSensitivity(nameValueList[0], nameValueList[1])
                if debug:
                    print "add base classification sensitivity %s %s\n" % (nameValueList[0], nameValueList[1])
            else:
                domain.addSensitivity(nameValueList[0], nameValueList[1])
                if debug:
                    print "add domain sensitivity %s %s\n" % (nameValueList[0], nameValueList[1])
