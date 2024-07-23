#!/usr/bin/env python
import sys
from jobs_linkedin.crew import JobsLinkedinCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {"applicant_resume":  """
        <PUT YOUR RESUME HERE>
        """
      }
    JobsLinkedinCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"applicant_resume":  """
        <PUT YOUR RESUME HERE>
        """
      }
    try:
        JobsLinkedinCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
