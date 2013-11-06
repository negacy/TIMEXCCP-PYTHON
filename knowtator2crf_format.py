'''
takes input xml files which is output of knowtator and extracts features which fits mallet CRF format
CRF format is:
<feature1><feature2> ... <featureN><label>

'''
 
import xml.etree.ElementTree as ET
import os
import nltk
import codecs

path = './tmp.in.xml.demo'#del' #parent directory of the xml files. All xml files are assumed to be in a single directory

mention_modifiers = ['early', 'mid', 'late', 'early-mid']

mention_indicative_words = ['arrest', 'arrests', 'phase', 'phases', 'entery', 'enter']

mention_punc = ['-', '/', ',', "'"]

pos_windowsize = 3 #windows size for part-of-speech tagging

for file in os.listdir(path):
        current_file = os.path.join(path, file)
        print current_file, file[:-14]
	outputFile = open('tmp.out.demo/'+file.strip('.xml') +'.txt', 'w')
	print ' '
	
	mention_id = []
	mention_start = []
	mention_end = []
	mention_text = []
	mention_label = []
	mentionSlot_id = []
	mentionSlot_val = []
	mention_slot = {} #dictionary decleration. classMetion id's are the keys and hasSlotMention ids the values
	mention_slot_id_ordered = [] #classmention id wise ordered.

        tree = ET.parse(current_file)
        root = tree.getroot()
	for element in root:#.find('annotation'):
		if element.tag == 'annotation':
			for child_tag in element:
				if child_tag.tag == 'mention':
					mention_id.append(child_tag.attrib['id'])
					#print child_tag.attrib['id']
				if child_tag.tag == 'span':
					mention_start.append(child_tag.attrib['start'])
					mention_end.append(child_tag.attrib['end'])
					#print 's: ', child_tag.attrib['start'], 'e: ', child_tag.attrib['end']
				if child_tag.tag == 'spannedText':
					mention_text.append(child_tag.text)
					#print child_tag.text
		
	for element in root:
		if element.tag == 'classMention':
			tmp_key = element.attrib['id']
			tmp_val = []
			for slotMention in element.iter('hasSlotMention'):
				tmp_val.append(slotMention.attrib['id'])
			mention_slot[tmp_key] =  tmp_val
			mention_slot_id_ordered.append(tmp_key)

	mention_slot_attrib = {}
	tmp_val = []
	tmp_id = []	
	for element in root:
		if element.tag == 'stringSlotMention':
			tmp = {}
			for i in mention_slot:
				count = 0
				for j in mention_slot[i]:
					if j == element.attrib['id']:
						if element[0].attrib['id'] == 'val':
							tmp_val.append(element[1].attrib['value'])
						if element[0].attrib['id'] == 'mod':
							tmp_id.append(element[1].attrib['value'])
							count += 1
						if len(mention_slot[i]) == 1 :
							tmp_id.append(0)
	k = 0
	for i in mention_slot_id_ordered:
		mention_slot_attrib[i] = [tmp_val[k], tmp_id[k]] 			
		k +=1
	

	k = 0	
	for i in mention_id:
		for j in mention_slot:
			if i == j:
				print j, mention_slot_attrib[j], '|', mention_id[k], mention_text[k], mention_start[k], mention_end[k]
				k +=1
	#
	# FEATURE EXTRACTION STARTS HERE.
	#
	'''
	open the source file to extract features. This module uses the span start and end point to identify the sentence which the specific mention
	'''
	data = codecs.open('./tmp.in.source/'+ file[:-14], 'r', 'utf-8').read()
	#data = codecs.open('./pubmed_abstracts/200_negative_samples.new/' + file[:-14], 'r', 'utf-8').read()
	
	#tag the data

	data_vec = data.split()
	mention_tag = nltk.pos_tag(data_vec)
	linearCounter = 0	
	k = 0
	#print 'mention tag: ', mention_tag
	#print 'len: ', len(mention_tag), len(data_vec)
	for word in data_vec:
		chk = 0
		print  k, word,
		try:
			#outputFile.write(str(k))
			#outputFile.write(' ')
			outputFile.write(word)
			outputFile.write(' ')
			#word themselves are features
			outputFile.write(word)
			outputFile.write(' ')
		except UnicodeEncodeError:
			unicodestr = word.encode('utf-8')
			outputFile.write(unicodestr)
			outputFile.write(' ')
			outputFile.write(unicodestr)
			outputFile.write(' ')
		'''
		word level features---case
		'''
		#F1. starts with a capital letter
		if len(word) > 0:
			print int(word[0].isupper()),
			outputFile.write(str(int(word[0].isupper())))
			outputFile.write(' ')
		#F2. word is all uppercase
		print int(word.isupper()),
		outputFile.write(str(int(word.isupper())))
		outputFile.write(' ')
		#F3. word is mixed case

		'''
		word level features---punctuation
		'''
		#F1. contains punctuation marks
		for p in mention_punc:
			if p in word:
				print 1,
				outputFile.write(str(1))
				outputFile.write(' ')
			else:
				print 0,
				outputFile.write(str(0))
				outputFile.write(' ')
		
		'''
		word level features---digit
		'''	
		#F1. word is digit
		print int(word.isdigit()),
		outputFile.write(str(int(word.isdigit())))
		outputFile.write(' ')
		#F2. word has digit
		chk_digit = 0
		for w_digit in word:
			if w_digit.isdigit():
				chk_digit = 1
				break

		if chk_digit:
			print 1,
			outputFile.write(str(1))
			outputFile.write(' ')
		else:
			print 0,
			outputFile.write(str(0))
			outputFile.write(' ')
		
		'''
		word level features---word length
		'''
		print len(word),
		outputFile.write(str(len(word)))
		outputFile.write(' ')
		'''
		check if there is one of the mention_indicatives after token. Handles G1 phase, G1 arrest.
		'''	
		if  len(data_vec) > (linearCounter + 1) and data_vec[linearCounter + 1] in mention_indicative_words:
			print data_vec[linearCounter +1],
			outputFile.write(data_vec[linearCounter + 1])
			outputFile.write(' ')
		else:
			print 0,
			outputFile.write(str(0))
			outputFile.write(' ')
		'''
		extracts PoS of words before the token
		'''
		for w in reversed(range(pos_windowsize)):
			if linearCounter - w >= 0:
				print   mention_tag[linearCounter - w][1], #PoS taggs are also features.
				outputFile.write(mention_tag[linearCounter - w][1])
				outputFile.write(' ')
			else:
				print 'NONE',
				outputFile.write('NONE')
				outputFile.write(' ')
		'''
		extracts PoS after token
		'''
		for w in range(1, pos_windowsize):
			if linearCounter + w < len(data_vec):
				print   mention_tag[linearCounter + w][1],
				outputFile.write(mention_tag[linearCounter + w][1])
				outputFile.write(' ')
			else:
				print 'NONE',
				outputFile.write('NONE')
				outputFile.write(' ')
		'''
		extract infromation annotated using knowtator
		'''
		for i in range(0, len(mention_start)): 
			if int(k) == int(mention_start[i]):
				if  word in mention_modifiers:
					print mention_text[i] , #token has mention
					print 0, #token doesn't have modifer
					print  mention_slot_attrib[mention_id[i]][0], #val of mention 
					print 'B_TIMEXCCP', #moifier, annotated_val, label. Modifier is beginning of mention
					try:
						outputFile.write(mention_text[i])
					except UnicodeEncodeError:
						unicodestr = mention_text[i].encode('utf-8')
						outputFile.write(unicodestr)
					outputFile.write(' ')
					outputFile.write(str(0))
					outputFile.write(' ')
					outputFile.write(mention_slot_attrib[mention_id[i]][0])
					outputFile.write(' ')
					outputFile.write('B_TIMEXCCP')
				else:
					print mention_text[i], mention_slot_attrib[mention_id[i]][1], mention_slot_attrib[mention_id[i]][0], 'B_TIMEXCCP',
					try:
						outputFile.write(mention_text[i])
					except UnicodeEncodeError:
						unicodestr = mention_text[i].encode('utf-8')
						outputFile.write(unicodestr)
					outputFile.write(' ')
					outputFile.write(str(mention_slot_attrib[mention_id[i]][1]))
					outputFile.write(' ')
					outputFile.write(mention_slot_attrib[mention_id[i]][0])
					outputFile.write(' ')
					outputFile.write('B_TIMEXCCP')
				chk = 1
			if int(k+len(word)) == int(mention_end[i]) and not int(k) == int(mention_start[i]): #handles calses like early metaphase.
				print mention_text[i], mention_slot_attrib[mention_id[i]][1], mention_slot_attrib[mention_id[i]][0], 'I_TIMEXCCP',
				outputFile.write(mention_text[i])
				outputFile.write(' ')
				outputFile.write(str(mention_slot_attrib[mention_id[i]][1]))
				outputFile.write(' ')
				outputFile.write(mention_slot_attrib[mention_id[i]][0])
				outputFile.write(' ')
				outputFile.write('I_TIMEXCCP')
				chk = 1
			elif  int(k) > int(mention_start[i]) and int(k+len(word)) < int(mention_end[i]): #handles early G2/m checkpoingl
				print 'xox'*10,
				outputFile.write(mention_text[i])
				outputFile.write(' ')
				outputFile.write(str(mention_slot_attrib[mention_id[i]][1]))
				outputFile.write(' ')
				outputFile.write(mention_slot_attrib[mention_id[i]][0])
				outputFile.write(' ')
				outputFile.write('I_TIMEXCCP')
				chk = 1
		if not chk:
			print 0,#token doesn't have mention
			print 0, #token doesn't have modifier
			print 0, #null val for non-mentions
			print 'O', #if word doesn't have label, assigned O.
			outputFile.write(str(0))
			outputFile.write(' ')
			outputFile.write(str(0))
			outputFile.write(' ')
			outputFile.write(str(0))
			outputFile.write(' ')
			outputFile.write('O')
		k = k + len(word) + 1
		linearCounter += 1
		print
		outputFile.write('\n')
	print
	#print 's: ', mention_start
	#print 'e: ', mention_end
	
	outputFile.close()

