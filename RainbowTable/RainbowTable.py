# Name:     Ang Qi Shao, Benjamin
# UOWID:    6857772
# Assignment 1 Part 2

# Import
from hashlib import md5

class RainbowTable:
    def __init__(self, password = "", hashVal = "", reduceVal = ""):
        self.W = password
        self.H = hashVal
        self.R = reduceVal

    # Q1P1
    # Get a list of all lines
    def _totalPassword(self):
        file = open(r'Wordlist.txt')
        lines = [line.strip() for line in file if line != "\n"]
        file.close()

        return lines

    # Function to generate hash
    def _generateHash(self, input):
        m = md5()
        m.update(input.encode('utf-8').strip())
        hashed = m.hexdigest()

        return hashed

    # Function to reduce hash value
    def _reduceFunc(self, hashed, total):
        length = len(total)
        reduced = int(hashed, 16) % length

        return reduced
    
    # Read file
    def _readNprocess(self):
        # Rainbow list
        rainbow = []

        # This will count every password
        counter = 0

        # A list container to store and return for this function
        listOfPassword = []

        # Read the file
        with open(r'Wordlist.txt', encoding = 'utf-8') as file:

            for line in file:
                counter += 1
                
                pw = line.strip()

                # Get total password
                total = self._totalPassword()

                # Generate hash function
                hashed = self._generateHash(pw)

                # Reduction function
                reduced = self._reduceFunc(hashed, total)

                # Fill each password with the set class and append it into a list
                each = RainbowTable(pw, hashed, reduced)
                listOfPassword.append(each)

                '''# Display all password, hash value, reduced value
                print("Number: {:<10} Password: {:<5}".format(counter, pw))
                print("Hashed value: {:^15}".format(hashed))
                print("Reduced value: {:^15}".format(reduced))
                print()'''

        print("Total number of password: {}".format(len(total)))
        file.close()

        return listOfPassword

    # Input hashed chain into Rainbow Table then output into 'Rainbow.txt'
    # P1Q2 - P1Q4
    def _rainbowChain(self):
        RT = {}
        marked = []
        allPW = self._totalPassword()

        with open('Rainbow.txt', 'w') as outFile:
            for index, password in enumerate(allPW):
                if index in marked:
                    continue

                marked.append(index)
                currW = password

                # Q1P2a generate the new hash value
                currH = self._generateHash(currW)

                # Q1P2bc reduce current hash and repeat reduce four times
                for j in range(0, 4):
                    reduced = self._reduceFunc(currH, allPW)
                    currW = allPW[reduced]
                    marked.append(reduced)
                    currH = self._generateHash(currW)

                # Q1P2d storing hash entry into rainbow table
                RT[password] = currH

                # Q1P3 sorting rainbow table based on the hash values
                RT = dict(sorted(RT.items()))

                # Q1P4 writing into file
                outFile.write('{:<20} {}\n'.format(password, currH))
        return RT

    # Q2P1 - Q2P2
    # Check if hash value given is in Rainbow Table, if not reduce and hash until you do
    def _checkHash(self, input):
        counter = 0
        OGinput = input
        allPW = self._totalPassword()
        rainbow = self._rainbowChain()
        password = ""
        # Q2P2 reduce and hash if hash value given is not in Rainbow Table
        while input not in rainbow.values() and counter != 548:
            print("{} not found".format(input))
            reduced = self._reduceFunc(input, allPW)
            password = allPW[reduced]
            input = self._generateHash(password)
            counter += 1
        else:
            password = list(rainbow.keys())[list(rainbow.values()).index(input)]
            
            # Q2P1 check if the Rainbow Table contains the Hash value
            print("Hash value {} is found in Rainbow Table".format(input))

        password = list(rainbow.keys())[list(rainbow.values()).index(input)]
        input = self._generateHash(password)

        # Q2P3 hash until the pre-image is found
        counter = 0
        allPW = self._totalPassword()
        while OGinput != input and counter != 548:
            reduced = self._reduceFunc(input, allPW)
            password = allPW[reduced]
            input = self._generateHash(password)
            counter += 1
        
        '''if counter != 548:
            # Q2P4 output the pre-image if can be found
            print()
            print("RESULT -- The pre-image is: {:>10}".format(password))
        else:
            # Q2P4 output the pre-image if cannot be found 
            print()
            print("RESULT -- The pre-image CANNOT be found")'''


if __name__ == '__main__':
    print()
    rain = RainbowTable()
    rain._readNprocess()
    rain._rainbowChain()
    print()
    print("The number of element in Rainbow Table: {:<10}".format(len(rain._rainbowChain())))
    print()

    # Ask user for hash value for pre-images Q2
    givenHash = input("Enter hash values for pre-images: ")
    print()

    # Check if the hash value given is empty
    print("Process...")
    if givenHash:
        reducedHash = rain._checkHash(givenHash)
    else:
        print("Please input the hash value")
        print("Exiting...")

    print()
    print("Press enter to exit...")
    input()

        

    


    
    
