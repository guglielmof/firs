
<h1>Firs: a (python) Framework for Information Retrieval Systems.</h1>

Firs is a python package, based on pyterrier, developed to help experimentation in Information Retireval.

Firs have multiple functions:
<ul>
  <li> It allows to import and evalutate traditional TREC collections </li>
  <li> It allows to compute an experimental Grid of Points (GoP) </li>
  <li> It allows to compute and handle replicates (such as shards or reformulations) </li>
</ul>


<h2>Install</h2>

To install firs, use the pip command:

<code>pip install firs</code>


<h2>The configuration file</h2>

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

<h2>Initializing firs</h2>
Once the configuration file is ready, it is possible to start working with firs.

Import firs and configure it:
```
import firs
firs.configure(<path to configuration file>)
```


<h2>Iporting a collection</h2>




<h2>Replicates</h2>

<h3>Shardings</h3>

<h3>Reformulations</h3>
