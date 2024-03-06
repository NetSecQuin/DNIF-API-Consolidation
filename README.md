# DNIF API Consolidation
*THIS IS NOT AN OFFICIAL DNIF PROJECT OR REPOSITORY*

The DNIF Hypercloud APIs allow users to query data through a series of three seperate APIs. 

There three APIs can be explained as:

Invoke: Run a data query and have a task id returned

Get Status: Get the status of a task through its task id (running, completed, failed)

Get Results: Output the results from the query

This script aims to utalize each of these API requests in order to, run a query, wait for its completion and provide its results in unison. 
It works by running the query, using a loop to verify that the returned task is completed, then requests the results. 
