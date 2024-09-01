# Linear Binary Programming Approach to Swiss Chess Pairing

### Description
This program presents an algorithm designed to provide a more straightforward and easy-to-understand implementation of USCF Swiss-style pairing for chess tournaments. The core of this algorithm utilizes Linear Binary Programming to optimize the pairings according to the USCF rules. This repository contains two pairing algorithms:

1. **realistic_optimization:** This algorithm is specifically designed to match the rules laid out by the USCF. It involves multiple steps, each utilizing linear binary programming to successively narrow down possible pairings until an optimal USCF-compliant pairing is achieved.

2. **experimental_optimization:** This is an experimental approach to Swiss Pairing. While it does not adhere to the designated USCF rules, it offers an alternative approach that may be perceived as more fair. It involves fewer hard constraints on pairing, allowing the linear binary programming aspect to function more freely. This method involves a single step and may yield slightly different results.