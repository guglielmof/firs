
<h1>firs: a (python) Framework for Information Retrieval Systems.</h1>

Firs is a python package, based on pyterrier, developed to help experimentation in Information Retireval.

Firs have multiple functions:
<ul>
  <li> It allows to import and evalutate traditional TREC collections </li>
  <li> It allows to compute an experimental Grid of Points (GoP) </li>
  <li> It allows to compute and handle replicates (such as shards or reformulations) </li>
</ul>

<h2>Setting firs up</h2>

<h3>Install</h3>

To install firs, use the pip command:

<code>pip install firs</code>


<h3>The configuration file</h3>

To work, firs relies on a configuration file. The configuration file needs a section for the paths and a section for each of the collections that you want to work on. In the "path" section, it is mandatory to specify the path to the jdk. Notice that, firs is based on pyterrier and therefore requires a jdk ≥ 11.


an example of configuration file:
```
[paths]
JAVAHOME = /usr/lib/jdk-11.0.11

[collections.robust04]
runs_path = ./data/TREC/TREC_13_2004_Robust/runs/
qrel_path = ./data/TREC/TREC_13_2004_Robust/pool/qrels.robust2004.txt
coll_path = ./EXPERIMENTAL_COLLECTIONS/TIPSTER/CORPUS
shrd_path = ./data/shardings/

[collections.trec08]
runs_path = ./data/TREC/TREC_08_1999_AdHoc/runs/all/
qrel_path = ./data/TREC/TREC_08_1999_AdHoc/pool/qrels.trec8.adhoc.txt
shrd_path = ./data/shardings/
```

Non-public elements, such as the qrels, are not provided by firs. They need to be placed in the path specified in the configuration file. In any cases, firs can used to build runs and grid of points starting from a collection. 

<h3>Initializing firs</h3>
Once the configuration file is ready, it is possible to start working with firs.

Import firs and configure it:
```
import firs
firs.configure(<path to configuration file>)
```

<h2>firs as Collections Manager</h2>

<h3>Importing a Collection</h3>

To import a trec collection,  run

```
#import the metadata of the collection
collection = firs.TrecCollection(collectionName=<name of the collection>)

#import the collection: the operation might be very time consuming
collection = collection.import_collection()
```

The function ```import_collection``` takes ```nThreads``` as additional parameter to import the runs in a parallel fashon. If you want to import the runs using 10 processors, do:

```
collection = collection.import_collection(nThreads=10)
```


<h3>Computing measures</h3>
To compute the measures on the selected collection, using the given qrels, run:
```
measures = collection.evaluate()
```
Notice that, this command assumes to have the full collection available (qrels alongside runs) and imported.

In some cases, the number of runs might be extremely high and it might be preferable to compute the measure run by run on the fly, avoiding to load all the runs. 
By running

```
measures = collection.parallel_evalutate(nThreads=<number of threads>)
```
It is possible to compute the measure in a parallel fashon and without preloading all the runs. 

Finally, it might be preferable, if available, to directly import a measure file. The path to the measure file need to be specified in the configuration file, under the proper collection, using the label ```msrs_path=path to the csv containing the measures```.
Using the command:

```
measures = collection.import_measures()
```
It is possible to directly import the proper measure file.
Notice that, using either ```parallel_evaluate``` and ```import_measures``` there is no need to run ```import_collection``` on the collection object before.

<h3>Replicates</h3>

Replicates represent multiple istances of the same experiment. An experiment is characterized by a subject (in IR, usually a topic) and the experimental conditions (in IR, usually the system used). Several approaches have been proposed to obtain the replicates. The simplest possible consists in considering human-made query reformulations. Note that, we do not provide any kind of dataset containing replicates: we only provide a strategy to handle them. A second approach consists in using reformulations. 

<h4>Shardings</h4>

The sharding procedure consists in inflating the number of observations by splitting the corpora into multiple subcorpora and running a specific experiment (a system applied to a specific query) multiple times, over each of the subcorpora.

A sharding on a collection is characterized by 3 elements:
<ul>
  <li>The number of shards</li>
  <li>The number of documents in each shard</li>
  <li>Whether shards are allowed or not</li>
</ul>

By calling:
```
sharding = firs.Shuttering(collection, sampling=<type of sampling>, nShards=<number of shards>, emptyShards=<empty label>)
```

Is it possible to obtain a sharding of the collection. A sharding is practically identical to a collection object, with the difference that both the qrel and the runs are splitted according to a division of the collection into shard.
The instruction:
```
sharded_measure = sharding.evaluate()
```
allows to evaluate the systems on the sharded collection.

Concerning the arguments passed to the constructor of the sharding, we have that:
<ul>
  <li><code>sampling</code>: it can be either <code>EVEN</code>where all the shards will be equal or <code>RNDM</code> where different shards can heve different lenghts</li>
  <li><code>nShards</code>: it needs to be an integer number</li>
  <li><code>emptyShards</code>: it can have either one of <code>E</code>, which allows to have shards without any relevant document or <code>NE</code>, in which every shard shoud have at least one relevant document for each of the topic</li>
</ul>

<h4>Reformulations</h4>


<h2> firs as Grid of Points (GoP) Experimental tool </h2>

<h3>The configuration file</h3>
Besides the information on the collection, to obtain a Grid of Points, the configuration file needs to be updated with some additional sections

```
[GoP]
stoplists = <list of comma-separated stoplists>
stemmers = <list of comma-separated stemmers>
models = <list of comma-separated models>
queryexpansions = <list of comma-separated query expansion models>

[stoplists]

stoplist.stoplist1 = <path to the stoplist>

stoplist.stoplist2 = <path to the stoplist>

[stemmers]

stoplist.stemmer1 = <name of the terrier class implementing the stemmer 1>

stoplist.stemmer2 = <name of the terrier class implementing the stemmer 2>


[models]

model.BM25.type = terrier
model.BM25.class = BM25


model.custommodel.type = python
model.custommodel.class = path/to/custommodel/class.py


[queryexpansions]

queryexpansions.RM3.type = terrier
queryexpansions.RM3.class = RM3

queryexpansions.custommodel.type = python
queryexpansions.custommodel.class = path/to/custommodel/class.py


```
Use the keyword <code>none</code> to avoid using a specific component (possible only for the stoplist, the stemmer and the query expansion model).

<h3>Indexing</h3>

To index a collection, add a new variable in the configuration file under the collection you wish to index

```
indx_path = /path/to/where/to/put/the/indexes
```

after the collection object has been preloaded with the command <code>collection = firs.TrecCollection(collectionName="name of the collection")</code>, it is possible to index it simply doing
  
```
firs.index_collection(coll, nThreads=<default 1>)
``` 

<h3>Retrieving</h3>

To retrieve a set of topics, it is first necessary to import a pandas with the topics. to do so, add an additional field to the configuration file, under the collaction that you wish to retrieve documents for: 

```
topic_parser = pandas_csv_reader
```

this configuration parameter specifies which parser to  use to read the topics. 



