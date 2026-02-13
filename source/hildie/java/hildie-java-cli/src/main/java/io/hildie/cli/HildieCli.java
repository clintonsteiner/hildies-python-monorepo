package io.hildie.cli;

import io.hildie.HildieLibrary;

/**
 * Hildie Java CLI
 */
public class HildieCli {

    public static void main(String[] args) {
        if (args.length == 0) {
            System.out.println("Usage: hildie-cli <name>");
            System.exit(1);
        }

        String name = args[0];
        System.out.println(HildieLibrary.greet(name));
    }
}
