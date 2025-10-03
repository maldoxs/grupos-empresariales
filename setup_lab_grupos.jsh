/*****************************************************
 * setup_lab_grupos.jsh
 * Script para inicializar el grafo GRUPOS_EMPRESARIALES
 * Ejecutar dentro del cliente `opg4j`
 *****************************************************/

import java.sql.DriverManager;
import oracle.pg.rdbms.pgql.PgqlConnection;
import java.nio.file.*;
import java.util.function.Consumer;

// Configuración de la conexión a tu base de datos Oracle
var jdbcUrl = "jdbc:oracle:thin:@//aquiles001.sii.cl:1525/grafosdb";
var user    = "beuser";
var pass    = "sii#2024";

// Crear conexiones
var conn    = DriverManager.getConnection(jdbcUrl, user, pass);
conn.setAutoCommit(false);
var pgql    = PgqlConnection.getConnection(conn);
var pgqlStmt = pgql.createStatement();

System.out.println("✅ Conectado a Oracle y PGQL listo para el nuevo modelo.");

// Eliminar el grafo GRUPOS_EMPRESARIALES si ya existe
try {
    pgqlStmt.execute("DROP PROPERTY GRAPH GRUPOS_EMPRESARIALES");
    System.out.println("🗑️ Grafo GRUPOS_EMPRESARIALES anterior eliminado.");
} catch (Exception e) {
    System.out.println("⚠️ Grafo GRUPOS_EMPRESARIALES no existía (continuamos).");
}

// Leer el archivo .pgql y crear el nuevo grafo
var script = Files.readString(Paths.get("scripts/create_grupos_empresariales.pgql"));
pgql.prepareStatement(script).execute();

System.out.println("✅ Grafo GRUPOS_EMPRESARIALES creado desde el script.");

// Helper para ejecutar consultas PGQL.
// ¡IMPORTANTE! Recuerda incluir "FROM GRUPOS_EMPRESARIALES" en tus consultas.
Consumer<String> query = q -> {
  try (var stmt = pgql.prepareStatement(q)) {
    stmt.execute();
    stmt.getResultSet().print();
  } catch (Exception e) {
    System.err.println("❌ Error en consulta: " + e.getMessage());
  }
};

System.out.println("✅ Función `query.accept(...)` lista para usar en el nuevo grafo.");
