'''
this program takes two files which have labels as a single vector and computes 
micro and macro avg.A detailed description about macro and micro avg is 
available at http://rushdishams.blogspot.com/2011/08/micro-and-macro-average-of-precision.html 
'''
import sys

def EvalMetrics(goldLabel, predictLabel):
	#count true positives
        tp = 0 
        fp = 0 
        fn = 0 
	
	m = len(goldLabel)
	#print 'm: ', m
        for i in range(0, m): 
                if goldLabel[i] == predictLabel[i] and goldLabel[i] != 'O':
                        tp += 1
                elif predictLabel[i] != 'O' and goldLabel[i] != predictLabel[i]:
                        fp += 1 
                        #print 'p: ', predictLabel[i], 'g: ', goldLabel[i]
                elif predictLabel[i] == 'O' and goldLabel[i] != 'O':
                        fn += 1
                        #print 'p: ', predictLabel[i], ' g: ', goldLabel[i]     
        print 'tp: ', tp, ' fp: ', fp, ' fn: ', fn
        precision = float(tp)/(tp+fp)
        recall = float(tp)/(tp+fn)
        fscore = 2*precision*recall/(precision + recall)
        print 'precision: ', precision
        print 'recall: ', recall
        print 'F-score: ', fscore
	print
	print
def conceptLevelMetrics(goldLabel, predictLabel, token, m, concept):
	predictLabel_concept = []
	goldLabel_concept = []

        #one-vs-all technique to compute metrics to a specific concept c.
        # list of concepts:
        #'interphase', 'G0', 'G1', 'S', 'synthesis', 'G2', 'mitosis', 'M', 
        #'anaphase', 'metaphase', 'prophase', 'telophase', 'checkpoint'
        #
        #
        '''
        update lable for predicted data ----one vs all
        rule-based to identify time expressions
        '''
	for i in range(0, m): 
		if predictLabel[i] != 'O':
			if concept not in ['S', 'M']:
				if concept.lower() in token[i].strip().lower():
					predictLabel_concept.append(predictLabel[i])
				else:
					predictLabel_concept.append('O')
			elif concept == 'M':
				if concept in token[i] and token[i].lower() != 'mitosis' and token[i].lower() != 'metaphase':
					predictLabel_concept.append(predictLabel[i])
					print 'Token M: ', token[i]
				else:
					predictLabel_concept.append('O')
			elif concept == 'S':
				if concept in token[i] and token[i].lower() != 'synthesis':
					predictLabel_concept.append(predictLabel[i])
					print 'Token S: ', token[i]
				else:
					predictLabel_concept.append('O')
					
		else:
			predictLabel_concept.append('O')    
	''' 
	update label for gold data --- one vs all
	rul-based to identify the time expressions
	'''

	for i in range(0, m): 
		if goldLabel[i] != 'O':
			if concept not in ['S', 'M']:
				if concept.lower() in token[i].strip().lower():
					goldLabel_concept.append(goldLabel[i])
				else:
					goldLabel_concept.append('O')
			elif concept == 'M':
				if concept in token[i] and token[i].lower() != 'mitosis' and token[i].lower != 'metaphase':
					goldLabel_concept.append(goldLabel[i])
				else:
					goldLabel_concept.append('O')
			elif concept == 'S':
				if concept in token[i] and token[i].lower() != 'synthesis':
					goldLabel_concept.append(goldLabel[i])
				else:
					goldLabel_concept.append('O')
		else:
			goldLabel_concept.append('O')
	print
	''' 
	call micro avg for ontology
	'''
	print concept
	EvalMetrics(goldLabel_concept, predictLabel_concept)                          


def main():
	if len(sys.argv) != 3:
		print 'Usage: ./evaluationMetrivcs.py <gold.txt> <predict.txt>'
	else:
		print 'gold label: ', sys.argv[1]
		print 'predicted label is read from: ', sys.argv[2]
		print 'xox'*20
		
		goldLabel = []
		predictLabel = []
		token = []
		
		concepts = ['interphase', 'G0', 'G1', 'S', 'synthesis', 'G2', 'mitosis', 'M', 'anaphase', 'metaphase', 'prophase', 'telophase', 'checkpoint']

		m = 0 #length of the test instance

		data = open(sys.argv[1]).readlines()
		for y in data:
			goldLabel.append(y.strip().split()[-1]) #last character in the dataset is label

		for x in data:
			token.append(x.strip().split()[0]) #first character in the dataset is token

		data = open(sys.argv[2]).readlines()
		for y in data:
			predictLabel.append(y.strip()) #argv[2] has only predict lable

			
		#print 'predict: ', predictLabel
		#print 'len: ', len(goldLabel), len(predictLabel)
		if len(goldLabel) == len(predictLabel):
			m = len(goldLabel)
		else:
			print 'There is error'	
			sys.exit()
		
	
		'''
		call metrics for macro avg.
		'''	
		EvalMetrics(goldLabel, predictLabel)

		'''
		evaluating individual concepts
		'''
		for i in concepts:
			conceptLevelMetrics(goldLabel, predictLabel, token, m, i)




if __name__ == "__main__":
	main()
