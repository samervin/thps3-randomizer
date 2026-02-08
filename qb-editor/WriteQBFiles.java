import java.io.*;
import java.util.*;
import java.util.stream.*;
import java.nio.file.*;
import java.nio.charset.*;
import javax.swing.*;
import javax.swing.text.*;
import java.nio.charset.Charset;

public class WriteQBFiles {

    private static Map<Integer, String> fields = null;
    private static SymbolListModel mainSymbolListModel = new SymbolListModel();
    private static Path outfileFolder = Paths.get("outfiles/");
    private static String dataFolder = "";

    public static void main(String[] args) throws IOException {
        // When running this code, be aware of the differences between Windows-1252 and UTF8.
        // Specifically, Windows-1252 stores the ¬ character (among others) as one byte (see https://en.wikipedia.org/wiki/Windows-1252),
        // but UTF-8 stores it as two. You might see additional or replaced characters if you have the wrong encoding.
        // The code in the other files, and possibly the QB format as a whole, seems to assume that all characters are one-byte only.
        // This blog post helped me understand the problem: https://medium.com/@andbin/jdk-18-and-the-utf-8-as-default-charset-8451df737f90
        // On java -version 21.0.2, this command correctly compiles and runs everything with the Windows-1252 encoding:
        // javac -encoding Cp1252 *.java && java -Dfile.encoding=COMPAT WriteQBFiles
        // You can also uncomment the below lines to learn more about the encoding that Java thinks it is using in which circumstances.
        // System.out.println("Java Runtime version " + System.getProperty("java.runtime.version"));
        // System.out.println("Charset.defaultCharset()                  = " + Charset.defaultCharset());
        // System.out.println("System.getProperty(\"file.encoding\")       = " + System.getProperty("file.encoding"));
        // System.out.println("System.getProperty(\"native.encoding\")     = " + System.getProperty("native.encoding"));
        // System.out.println("System.getProperty(\"sun.jnu.encoding\")    = " + System.getProperty("sun.jnu.encoding"));
        // System.out.println("System.getProperty(\"sun.stdout.encoding\") = " + System.getProperty("sun.stdout.encoding"));
        // System.out.println("System.getProperty(\"sun.stderr.encoding\") = " + System.getProperty("sun.stderr.encoding"));
        // System.out.println("System.console().charset()                = " + System.console().charset());

        // The dataFolder should be passed as the first argument, e.g. `java WriteQBFiles C:/Your/Folder/rando/Data/`
        dataFolder = args[0];
        System.out.println(dataFolder);

        // I don't get this new syntax so just make it an array
        Path[] paths = Files.walk(outfileFolder)
            .filter(Files::isRegularFile)
            .filter(file -> file.getFileName().toString().endsWith(".out"))
            .toArray(Path[]::new);
        for (Path path : paths) {
            String data = readWindowsFile(path);
            writeQbFile(data, outfileFolder.relativize(path));
        }
    }

    private static String readWindowsFile(Path path) throws IOException {
        // System.out.println("Reading " + outfileFolder.relativize(path));
        return Files.readString(path, Charset.forName("windows-1252"));
    }

    private static void writeQbFile(String data, Path path) {
        String pathString = dataFolder + path.toString().replaceAll(".out$", ".qb");
        System.out.println("Writing " + pathString);
        QbWriter qbWriter = new QbWriter(data, new File(pathString), new HashMap<Integer, String>());
        qbWriter.run();
    }
}
