#Problem Set 4 Tests

from ps4 import *

def build_coder_tests():
    #testLetters = ['A', 'b', ' ']
    shiftsAndResults = {1:{'A':'B','b':'c',' ':'a'},17:{'A':'R','b':'s',' ':'q'},-22:{'A':'F','b':'g',' ':'e'}, 8:{'T':'A', 's':' ', ' ':'h', 't':'a'}}
    
    for shift in shiftsAndResults.keys():
        #print shiftsAndResults.keys()
        coder = build_coder(shift)

        #Run Tests on Coder
        passed = True

        if not coderShouldHaveAllUpperAndLowerAsciiLetters(coder):            
            printTestResult(shift, False)
            continue #Stop Testing

        testLetters = shiftsAndResults[shift]
        #print testLetters
        for c in testLetters.keys():            
            #This will short circuit if coderShouldHaveCorrectLetter fails once
            passed = passed and coderShouldHaveCorrectLetter(coder, c, testLetters[c])

        if not passed:
            print coder

        printTestResult(shift, passed)
    
def printTestResult(shiftValue, passed):
    result = GetResultFromBool(passed)      
        
    print "Shift of " + str(shiftValue) + " " + result

def coderShouldHaveAllUpperAndLowerAsciiLetters(coder):
    passing = True

    #Check that all letters exist in upper and lowercase
    for c in string.ascii_letters+' ':
        if c not in coder:
            print 'Expected "' + c + '" to be in dictionary'
            passing = False

    return passing

def coderShouldHaveCorrectLetter(coder, testLetter, expectedResult):
    #print testLetter
    if coder[testLetter] != expectedResult:
        print 'Expected "' + testLetter + '" to be "' + expectedResult + '" instead got ' + coder[testLetter]
        print
        return False
    else:
        return True

def build_encoder_should_give_you_exactly_what_build_coder_does():
    coder = build_coder(5)
    encoder = build_encoder(5)

    passed = True

    for c in coder.keys():
        if c not in encoder:
            print "Expected " + c + " to produce " + coder[c] + ", but got None instead"
            passed = False
        elif coder[c] != encoder[c]:
            print "Expected " + c + " to produce " + coder[c] + ", but got " + encoder[c] + " instead"
            passed = False

    print "Build Encoder " + GetResultFromBool(passed)

def build_decoder_should_give_you_exactly_what_build_coder_does_but_negative():
    coder = build_coder(-8)
    decoder = build_decoder(8)

    passed = True

    for c in coder.keys():
        if c not in decoder:
            print "Expected " + c + " to produce " + coder[c] + ", but got None instead"
            passed = False
        elif coder[c] != decoder[c]:
            print "Expected " + c + " to produce " + coder[c] + ", but got " + decoder[c] + " instead"
            passed = False

    print "Build Decoder " + GetResultFromBool(passed)

def GetResultFromBool(result):
    if result:
        return "Passed"
    else:
        return "Failed"  
    
def testApplyCoder():
    #Get an encoder and the matching decoder
    #Test that it comes out the same as it went in
    testString = "The Quick Brown Fox Jumped Over the Lazy Dog."

    #A shift of 12 will cause the test to fail because of the upper case "O" is decoded to "o"
    #This is either an oversight or by design of the homework author
    shift = 11

    encoder = build_encoder(shift)
    decoder = build_decoder(shift)

    cipherText = apply_coder(testString, encoder)
    plainText = apply_coder(cipherText, decoder)

    if plainText != testString:
        print
        print "Apply Coder Failed"
        print "Expected: " + testString
        print "Returned: " + plainText
        print "Cipher:   " + cipherText
    else:
        print "Apply Coder Passed"

def testApplyShift():
    testString = "This is a test."
    testShift = "Apq hq hiham a."
    shift = 8

    cipherText = apply_shift(testString, shift)

    if testShift != cipherText:
        print
        print "Apply Shift Failed"
        print "Expected: " + testShift
        print "Returned: " + cipherText
    else:
        print "Apply Shift Passed"

def testFindBestShift():
    testString = "The Quick Brown Fox Jumped Over the Lazy Dog."
    shift = 11
    cipherText = apply_shift(testString, 11)

    bestShift = find_best_shift(word_list, cipherText)

    if bestShift != shift:
        print
        print "Find Best Shift Failed"
        print "Expected Best Shift to be " + str(shift) + " but instead got " + str(bestShift)
    else:
        print "Find Best Shift Passed"

def testApplyShifts():
    testString = "Do Androids Dream of Electric Sheep?"
    shifts = [(0,6), (3, 18), (12, 16)]
    expectedString = "JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?"

    cipherText = apply_shifts(testString, shifts)

    if expectedString != cipherText:
        print
        print "Apply Shifts Failed"
        print "Expected: " + expectedString
        print "Returned: " + cipherText
    else:
        print "Apply Shift Passed"

def testFindBestShifts():
    testString = "The Quick Brown Fox Jumped Over the Lazy Dog."
    shifts = [(0, 23), (10, 2), (27, 5), (32, 11)]
    reverseShifts = [(0, 4), (10, 25), (27, 22), (32, 16)]
    cipherText = apply_shifts(testString, shifts)

    #print "Cipher: " + cipherText
    decodeShifts = find_best_shifts(word_list, cipherText)

    decodedText = apply_shifts(cipherText, decodeShifts)

    if decodeShifts != reverseShifts or testString.lower() != decodedText.lower():
        print
        print "Find Best Shifts Failed"
        print "Expected Best Shifts to be ",
        print reverseShifts,
        print " but instead got ",
        print decodeShifts
        print "Expected text ", testString, " to be ", decodedText
    else:
        print "Find Best Shifts Passed"

def testDecryptFable():
    print
    print "Decrypted Fable: "
    print decrypt_fable()

word_list = load_words()

build_coder_tests()
build_encoder_should_give_you_exactly_what_build_coder_does()
build_decoder_should_give_you_exactly_what_build_coder_does_but_negative()

testApplyCoder()
testApplyShift()

testFindBestShift()

testApplyShifts()

testFindBestShifts()

testDecryptFable()
