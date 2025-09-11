/*****************************************************
 * setup-lab.jsh
 * Script para inicializar el laboratorio Oracle Graph
 * Ejecutar dentro del cliente `opg4j`
 *****************************************************/

import java.sql.DriverManager;
import oracle.pg.rdbms.pgql.PgqlConnection;
import java.nio.file.*;
import java.util.function.Consumer;

// Configurar conexión JDBC a Oracle
var jdbcUrl = "jdbc:oracle:thin:@//aquiles001.sii.cl:1525/grafosdb";
var user    = "beuser";      // <- actualizar si cambias el usuario
var pass    = "sii#2024";    // <- actualizar si cambias la clave

// Crear conexión a la base Oracle
var conn     = DriverManager.getConnection(jdbcUrl, user, pass);
conn.setAutoCommit(false);

// Crear conexión PGQL sobre esa conexión
var pgql     = PgqlConnection.getConnection(conn);
var pgqlStmt = pgql.createStatement();

System.out.println("✅ Conectado a Oracle y PGQL listo");

// Eliminar grafo HR_BE si existe
try {
    pgqlStmt.execute("DROP PROPERTY GRAPH HR_BE");
    System.out.println("🗑️ Grafo HR_BE eliminado");
} catch (Exception e) {
    System.out.println("⚠️ Grafo HR_BE no existía (continuamos)");
}

// Leer archivo .pgql y crear el grafo HR_BE
var script = Files.readString(Paths.get("scripts/create_be.pgql"));
pgql.prepareStatement(script).execute();

System.out.println("✅ Grafo HR_BE creado desde create_be.pgql");

// Crear helper para ejecutar consultas PGQL fácilmente
Consumer<String> query = q -> {
  try (var stmt = pgql.prepareStatement(q)) {
    stmt.execute();
    stmt.getResultSet().print();
  } catch (Exception e) {
    System.err.println("❌ Error en consulta: " + e.getMessage());
  }
};

System.out.println("✅ Función `query.accept(...)` lista para usar");
