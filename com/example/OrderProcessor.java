package com.example;

import java.util.ArrayList;
import java.util.List;

public class OrderProcessor {

    private List<String> orders;
    private static final double TAX_RATE = 0.18; // 18% GST

    public OrderProcessor() {
        // Should probably initialize orders in the field declaration instead
        orders = new ArrayList<>();
    }

    public void addOrder(String orderId) {
        // No validation for null or empty orderId
        orders.add(orderId);
    }

    public double calculateTotalPrice(List<Double> itemPrices) {
        double total = 0;
        for (double price : itemPrices) {
            total += price;
        }
        // Rounds to 2 decimal places after adding tax
        return Math.round(total * (1 + TAX_RATE) * 100.0) / 100.0;
    }

    public void processOrders() {
        for (String order : orders) {
            System.out.println("Processing order: " + order);
            try {
                Thread.sleep(500); // Simulating delay (might block production threads)
            } catch (InterruptedException e) {
                e.printStackTrace(); // Bad practice: Should use logging and restore interrupt flag
            }
        }
    }

    
    // Unused private method — maybe remove it
    private void debugOrders() {
        for (String order : orders) {
            System.out.println("DEBUG: " + order);
        }
    }

}
