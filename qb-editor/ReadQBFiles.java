import java.io.*;
import java.util.*;
import java.nio.file.*;
import java.nio.charset.*;
import javax.swing.*;
import javax.swing.text.*;
import java.nio.charset.Charset;

public class ReadQBFiles {

    private static Map<Integer, String> fields = null;
    private static SymbolListModel mainSymbolListModel = new SymbolListModel();
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

        // The dataFolder should be passed as the first argument, e.g. `java WriteQBFiles C:/Your/Folder/Data/`
        dataFolder = args[0];
        System.out.println(dataFolder);
        String data;

        String[] allScriptFilenames = {
            "airtricks.qb",
            "ajc_scripts.qb",
            "alf_scripts.qb",
            "alltricks.qb",
            "anim.qb",
            "bails.qb",
            // "bdj_goalscripts.qb", // This file is empty and unfortunately that breaks the parser
            "bdj_pedscripts.qb",
            "bdj_scripts.qb",
            "bird_a.qb",
            "bird_a_resting.qb",
            "bird_b.qb",
            "bird_b_resting.qb",
            "blue_flg.qb",
            "boardselect.qb",
            "buttonscripts.qb",
            "camera.qb",
            "cas.qb",
            "casmenu.qb",
            "casnames.qb",
            "cheats.qb",
            "cjr_scripts.qb",
            "compmenu.qb",
            "compress.qb",
            "comp_scripts.qb",
            "cpf_scripts.qb",
            "crowd_a.qb",
            "crowd_a_backrow.qb",
            "crowd_a_lod01.qb",
            "crowd_b.qb",
            "crowd_b_lod01.qb",
            "crowd_c.qb",
            "crowd_c_lod01.qb",
            "crowd_d.qb",
            "crowd_d_lod01.qb",
            "crowd_judge_a.qb",
            "crowd_judge_a_lod01.qb",
            "crowd_judge_b.qb",
            "crowd_judge_b_lod01.qb",
            "debug.qb",
            "debugmenu.qb",
            "dialogbox.qb",
            "edpieces.qb",
            "flags.qb",
            "frontend.qb",
            "frontendcamanims.qb",
            "game.qb",
            "gameflow.qb",
            "gamemode.qb",
            "gameoptions.qb",
            "girl_a.qb",
            "goal_scripts.qb",
            "grindlist.qb",
            "grindscripts.qb",
            "groundtricks.qb",
            "helper.qb",
            "horse.qb",
            "iniskater.qb",
            "iniskater_exceptions.qb",
            "iniskater_f.qb",
            "iniskater_secret.qb",
            "iniskater_shared.qb",
            "iniskater_team.qb",
            "iviewer.qb",
            "jku_scripts.qb",
            "js_scripts.qb",
            "judges.qb",
            "keyboard.qb",
            "levelmenu.qb",
            "levels.qb",
            "lights.qb",
            "liptricks.qb",
            "mainmenu.qb",
            "memcard.qb",
            "memcardmenu.qb",
            "memcardmessages.qb",
            "menu.qb",
            "menusounds.qb",
            "menutest.qb",
            "models.qb",
            "movies.qb",
            "net.qb",
            "netmenu.qb",
            "netmessages.qb",
            "nscustomparks.qb",
            "object.qb",
            "optionsmenu.qb",
            "panel.qb",
            "park_ed.qb",
            "ped.qb",
            "pedestrian_a.qb",
            "pedestrian_a_lod01.qb",
            "pedestrian_a_lod02.qb",
            "pedestrian_a_lod03.qb",
            "pedestrian_b.qb",
            "pedestrian_b_lod01.qb",
            "pedestrian_b_lod02.qb",
            "pedestrian_b_lod03.qb",
            "pedestrian_c.qb",
            "pedestrian_c_lod01.qb",
            "pedestrian_c_lod02.qb",
            "pedestrian_c_lod03.qb",
            "pedestrian_d.qb",
            "pedestrian_d_lod01.qb",
            "pedfem_a.qb",
            "pedfem_a_lod01.qb",
            "pedfem_b.qb",
            "pedfem_b_lod01.qb",
            "pedfem_c.qb",
            "pedfem_c_lod01.qb",
            "pedfem_d.qb",
            "pedfem_d_lod01.qb",
            "pedfem_e.qb",
            "pedfem_e_lod01.qb",
            "pedfem_f.qb",
            "pedfem_f_lod01.qb",
            "pedpro_cab.qb",
            "pedpro_campbell.qb",
            "pedpro_glifberg.qb",
            "pedpro_hawk.qb",
            "pedpro_koston.qb",
            "pedpro_lasek.qb",
            "pedpro_margera.qb",
            "pedpro_mullen.qb",
            "pedpro_muska.qb",
            "pedpro_reynolds.qb",
            "pedpro_rowley.qb",
            "pedpro_steamer.qb",
            "pedpro_thomas.qb",
            "ped_bbq_guy.qb",
            "ped_bbq_guy_lod01.qb",
            "ped_bully_a.qb",
            "ped_bully_a_lod01.qb",
            "ped_bum_a.qb",
            "ped_canada_a.qb",
            "ped_canada_a_lod01.qb",
            "ped_canada_a_lod02.qb",
            "ped_canada_a_lod03.qb",
            "ped_canada_b.qb",
            "ped_canada_b_lod01.qb",
            "ped_canada_b_lod02.qb",
            "ped_canada_b_lod03.qb",
            "ped_canada_c.qb",
            "ped_canada_c_lod01.qb",
            "ped_canada_c_lod02.qb",
            "ped_canada_c_lod03.qb",
            "ped_canada_d.qb",
            "ped_canada_d_lod01.qb",
            "ped_constr_a.qb",
            "ped_constr_a_lod01.qb",
            "ped_constr_b.qb",
            "ped_constr_b_lod01.qb",
            "ped_judge_1.qb",
            "ped_judge_3.qb",
            "ped_judge_5.qb",
            "ped_judge_a.qb",
            "ped_judge_b.qb",
            "ped_judge_c.qb",
            "ped_judge_d.qb",
            "ped_judge_e.qb",
            "ped_photoguy_a.qb",
            "ped_photoguy_a_lod01.qb",
            "ped_pirate_a.qb",
            "ped_richkid_a.qb",
            "ped_richkid_a_lod01.qb",
            "ped_security_a.qb",
            "ped_security_a_lod01.qb",
            "ped_security_b.qb",
            "ped_security_b_lod01.qb",
            "ped_skateshop.qb",
            "ped_surf01.qb",
            "ped_surf_a.qb",
            "ped_terrorist_a.qb",
            "ped_terrorist_a_lod01.qb",
            "ped_thinman_a.qb",
            "ped_thinman_axe.qb",
            "ped_thinman_a_lod01.qb",
            "ped_welder_a.qb",
            "ped_welder_a_lod01.qb",
            "ped_welder_b.qb",
            "ped_welder_b_lod01.qb",
            "physics.qb",
            "promenu.qb",
            "protricks.qb",
            // "qdir.txt", // This lists all available script files.
            // It supports relative folder structure, so e.g. '../new_folder/mainmenu.qb' works
            // It does not seem to support absolute folder structure, so 'C:/new_folder/mainmenu.qb' doesn't work
            // While THPS3.exe checks Data/Scripts/qdir.txt in its current working directory,
            // the filepaths are relative to the absolute location of THPS3.exe itself, NOT the current working directory
            "rebuildlevels.qb",
            "records.qb",
            "red_flg.qb",
            "replay.qb",
            "reverb.qb",
            "scaling.qb",
            "sfxmenu.qb",
            "sfx_car.qb",
            "sfx_ped.qb",
            "shark_a.qb",
            "sk3_pedscripts.qb",
            "sk3_scripts.qb",
            "skater.qb",
            "skater_m.qb",
            "skater_m_bails.qb",
            "skater_m_basics.qb",
            "skater_m_flatland.qb",
            "skater_m_flipgrab.qb",
            "skater_m_fliptricks.qb",
            "skater_m_grabtricks.qb",
            "skater_m_grind.qb",
            "skater_m_lip.qb",
            "skater_m_misc.qb",
            "skater_m_special.qb",
            "skater_profile.qb",
            "skater_sfx.qb",
            "skutils.qb",
            "soundtest.qb",
            "statsmenu.qb",
            "strings.qb",
            "teamcheat.qb",
            "terrain.qb",
            "terrorist_a.qb",
            "trickmenu.qb",
            "tricks.qb",
            "tutorials.qb",
        };

        String[] allLevelFilenames = {
            "Ap/ap.qb",
            "Burn/burn.qb",
            "Can/can.qb",
            "Can_Sky/can_sky.qb",
            "Foun/foun.qb",
            "LA/la.qb",
            "Rio/rio.qb",
            "Rio_Sky/rio_sky.qb",
            "Ros/ros.qb",
            "Ros_Sky/ros_sky.qb",
            "Shp/shp.qb",
            "Shp_Sky/shp_sky.qb",
            "SI/si.qb",
            "SI_Sky/si_sky.qb",
            "Sk3Ed_Bch/sk3ed_bch.qb",
            "Sk3Ed_Indr/sk3ed_indr.qb",
            "Sk3Ed_Schl/sk3ed_schl.qb",
            "Sk3Ed_Schl_Sky/sk3ed_schl_sky.qb",
            "SkateShop/skateshop.qb",
            "Sub/sub.qb",
            "Tok/tok.qb",
            "Tut/tut.qb",
            "Ware/ware.qb",
        };

        for (String filename : allScriptFilenames) {
            data = readQbFile("Scripts/" + filename);
            writeWindowsFile(data, "../vanilla-qbs/Scripts/" + filename);
        }

        for (String filename : allLevelFilenames) {
            data = readQbFile("Levels/" + filename);
            writeWindowsFile(data, "../vanilla-qbs/Levels/" + filename);
        }
    }

    private static void writeWindowsFile(String data, String pathString) throws IOException {
        System.out.println("Writing " + pathString);
        Files.createDirectories(Paths.get(pathString).getParent());
        Files.writeString(Paths.get(pathString), data, Charset.forName("windows-1252"));
    }

    private static String readQbFile(String pathString) throws IOException {
        System.out.println("Reading " + pathString);
        QbFileHandler reader = new QbFileHandler(new File(dataFolder + pathString));
        QbParser parser = new QbParser(reader.getByteStream());
        parser.getTablePosition();
        reader.createTable();
        parser.setFields(reader.getFields());
        return parser.parse();
    }
}
