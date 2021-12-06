#!/usr/bin/env python3
# MIT License

# Copyright (c) 2020 pixelbubble

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# based on https://github.com/pixelbubble/ProtOSINT/blob/main/protosint.py

def generate_accounts():
	firstName = input("First name: ").lower()
	lastName = input("Last name: ").lower()
	yearOfBirth = input("Year of birth: ")
	pseudo = input("Username (optional): ").lower()
	zipCode = input("Zip code (optional): ")

	results_list = []

	results_list.append(firstName+lastName)
	results_list.append(lastName+firstName)
	results_list.append(firstName[0]+lastName)
	results_list.append(lastName)
	results_list.append(firstName+lastName+yearOfBirth)
	results_list.append(firstName[0]+lastName+yearOfBirth)
	results_list.append(lastName+firstName+yearOfBirth)
	results_list.append(firstName+lastName+yearOfBirth[-2:])
	results_list.append(firstName+lastName+yearOfBirth[-2:])
	results_list.append(firstName[0]+lastName+yearOfBirth[-2:])
	results_list.append(lastName+firstName+yearOfBirth[-2:])
	results_list.append(firstName+lastName+zipCode)
	results_list.append(firstName[0]+lastName+zipCode)
	results_list.append(lastName+firstName+zipCode)
	results_list.append(firstName+lastName+zipCode[:2])
	results_list.append(firstName[0]+lastName+zipCode[:2])
	results_list.append(lastName+firstName+zipCode[:2])

	if pseudo:
		results_list.append(pseudo)
		results_list.append(pseudo+zipCode)
		results_list.append(pseudo+zipCode[:2])
		results_list.append(pseudo+yearOfBirth)
		results_list.append(pseudo+yearOfBirth[-2:])

	results_list = list(set(results_list))

	return results_list

if __name__ == '__main__':
	results = generate_accounts()
	print('\n'.join(results))