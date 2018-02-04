#!/bin/bash
#floyd run --gpu --mode jupyter --data moriano/datasets/cats-vs-dogs-augmented/1 --env tensorflow-1.4
floyd run --gpu --mode jupyter --data moriano/datasets/cats-vs-dogs-224x244x3/2 --env tensorflow-1.4
