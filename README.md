#Train Route Project (Directed Graph)

<h3>Python3 Directed Graph project for train routing</h3>

<p>The purpose of this project is to provide routing info for a train system initialized using graph description:</p>
AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7

<h4>trainRouteProject.py</h4>
<b>run:</b>python trainRouteProject.py</br>
<p>Considering this project seemed to consider how I would build the appropriate sorting and data structures required for this exercise, this script does not rely on any third party libraries and I've implemented my own, minimal, directed graphing, building and sorting. Recursion for node navigation is one of the primary functionalities. In reality, I would not re-implement these datastructures and features myself and instead would rely on a trusted, widely used third-party library. This would be to leverage a tried and tested solution, reduce testing overhead, and ideally see better performance gains using a module that executes in a lower level language with greater efficiency than base python provides.</p>

<h4>networkxexample.py</h4>
<b>run:</b>pip install networkx</br>
<b>run:</b>python networkxexample.py</br>
<p>Using the public, well-used <a href='https://networkx.org/'>NetworkX library</a> I've reproduced the above tests to ensure the same results are produced as in the homebrewed solution above. This closer mimics how I would implement this functionality in a real-world scenario.</p>