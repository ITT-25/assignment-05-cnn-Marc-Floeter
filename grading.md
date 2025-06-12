## Marc Flöter  (12.5/15P)

### 1. Exploring Parameters (4/5)
* selected hyperparameter values make sense
    * makes sense (1P)
* networks were trained correctly
    * training seems ok, even though sigmoid does weird stuff, ran your code again, and this weird behaviour does not occur any more -> maybe this is caused by an uneven distribution of categories in the train or test set (caused by *no_gesture*)(-0.5P)
* there are results
    * yep (1P)
* results are reported and visualized appropriately
    * `plot_accuracy_inference.png`: the legend overlays the important part of the plot 
    * no prior assumptions described (-0.5P)

### 2. Gathering a Dataset (3.5/5)
* sufficient images captured
    * all images at the same place (-0.5P)
* sufficient images annotated
    * yep (2P)
* annotations are compatible to the HaGRID dataset
    * yep (1P)
* confusion matrix
    * this would've been a fixable problem (-1P)

### 3. Gesture-based Media Controls (5/5)
* three hand poses are tracked and distinguished reliably 
    * you could've removed the peace gesture recognition
    * but else: nice! (2P)
* three media control features are implemented
    * yep (1P)
* mapping of gestures to media controls works and makes sense
    * yep (1P)
* low latency between gesture and the system’s reaction
    * yep (1P)