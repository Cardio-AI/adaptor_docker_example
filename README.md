# AdaptOR2022 MICCAI Challenge Docker Example

A docker example repository to support participants in creating submissions for
the [AdaptOR2022 MICCAI Challenge](https://www.synapse.org/AdaptOR_Challenge_2022_MICCAI).

- [Challenge Website](https://adaptor2022.github.io/)
- [Information on submission](https://adaptor2022.github.io/submissiondetails/)
- [Synapse Challenge](https://www.synapse.org/AdaptOR_Challenge_2022_MICCAI)
- [Submission Tutorial](https://www.synapse.org/#!Synapse:syn29340309/wiki/)

## Setup

1. The container can be built with

```
docker build --tag adaptor_challenge ./src/
```

2. The container can be run with
```
docker run --gpus all -v "<absolute_host_input_directory>:/input" -v "<absolute_host_output_directory>:/output" adaptor_challenge
```  

