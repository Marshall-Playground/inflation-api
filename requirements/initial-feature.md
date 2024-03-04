# Summary

I want a Java service that provides inflation rates of USD and changes in value of USD over time

# Constraints

- Write the code for the Spring Boot framework

- Use the latest features of Java 21

- Write clean code in accordance with the standards laid out in Robert Martin's book *Clean Code*

TODO: create service level requirements files to modify Java or to serve as initial inputs for generating
new code and tests

# Acceptance Tests

## Class `InflationRateService`

Dependencies:
  1. Use a CSV file containing inflation rates for every year as your input source

Public methods:
1. return the inflation rate of USD for a given year selectedYear
2. return the change in value of USD due to inflation between two years startYear and endYear as a number valueChangeFactor. 
   The result should satisfy the equation valueOfUsdInStartYear = valueChangeFactor * valueOfUsdInEndYear.
3. return the value of 1 USD from a year startYear in this year

