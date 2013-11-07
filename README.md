TIMEXCCP-PYTHON
===============

A python code to extract features for temporal classification

Individual file description:
	* runTrain.sh - a shell script to run mallet over a dataset. The input and outpfiles are listed in side the shall script
	*runTest.sh - shell script to run model generated from runTrain.sh
	*runEval.sh - evaluator.

Feature extraction	
	*knowtator2crf_format.py - 	takes input xml files which are output of knowtator and extracts features which fit mallet CRF format
   CRF format is:
   <token> <feature1><feature2> ... <featureN><label>

Evaluation
	* evaluationMetrics.py: this program takes two files which have labels as a single vector and computes micro and macro avg.A detailed description about macro and micro avg is  available at http://rushdishams.blogspot.com/2011/08/micro-and-macro-average-of-precision.html 


