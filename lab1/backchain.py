from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    #raise NotImplementedError
    results = [hypothesis]
    for rule in rules:
        conse = rule.consequent();
        for expr in conse:
            binding = match(expr, hypothesis)
            if binding or expr == hypothesis:
                ante = rule.antecedent()    
                if isinstance(ante,str):
                    new_hypothesis = populate(ante, binding)
                    results.append(backchain_to_goal_tree(rules, new_hypothesis))
                    results.append(new_hypothesis);
                else:                    
                    new_results = []
                    for statement in ante:
                        new_hypothesis = populate(statement, binding)
                        new_results.append(backchain_to_goal_tree(rules, new_hypothesis))
                    results.append(create_statement(new_results,ante));
    return simplify(OR(results))
                              
def create_statement(statements, rule):
    if isinstance(rule, AND):
        return AND(statements)
    elif isinstance(rule, OR):
        return OR(statements)
# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
