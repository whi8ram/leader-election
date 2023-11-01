from leader_election import LeaderElection

if __name__ == "__main__":
    leader_election = LeaderElection("localhost:2181")
    leader_election.run()
