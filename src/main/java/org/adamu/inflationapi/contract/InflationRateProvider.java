package org.adamu.inflationapi.contract;

public interface InflationRateProvider {

    double getInflationRateInYear(int selectedYear);

    double getChangeInValueBetweenTwoYears(int startYear, int endYear);
}
