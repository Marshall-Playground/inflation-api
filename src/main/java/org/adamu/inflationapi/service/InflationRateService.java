package org.adamu.inflationapi.service;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public final class InflationRateService implements InflationRateProvider {

        private Map<Integer, Double> inflationRates;

        public InflationRateService(String csvFilePath) {
            this.inflationRates = new HashMap<>();
            loadInflationRates(csvFilePath);
        }

        private void loadInflationRates(String csvFilePath) {
            try (BufferedReader br = new BufferedReader(new FileReader(csvFilePath))) {
                String line;
                while ((line = br.readLine()) != null) {
                    String[] parts = line.split(",");
                    int year = Integer.parseInt(parts[0]);
                    double rate = Double.parseDouble(parts[1]);
                    inflationRates.put(year, rate);
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        @Override
        public double getInflationRateInYear(int selectedYear) {
            return inflationRates.getOrDefault(selectedYear, 0.0);
        }

        @Override
        public double getChangeInValueBetweenTwoYears(int startYear, int endYear) {
            double inflationStart = getInflationRate(startYear);
            double inflationEnd = getInflationRate(endYear);
            return Math.pow(1 + inflationEnd, endYear - startYear) / (1 + inflationStart);
        }

        public double valueOfOneDollarNowFromPreviousYear(int startYear) {
            double result = 1.0;
            for (int year = startYear; year < 2022; year++) {
                double inflation = getInflationRate(year);
                result *= (1 + inflation);
            }
            return result;
        }
    }
}
