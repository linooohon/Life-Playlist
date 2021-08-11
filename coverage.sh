#!/bin/bash
coverage run test_coverage.py
coverage report -m
coverage html