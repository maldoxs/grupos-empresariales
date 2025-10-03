/*****************************************************
 * setup_lab_ge_model.jsh  (lab: crea + lee, sin publish)
 *****************************************************/
import java.sql.DriverManager;
import oracle.pg.rdbms.pgql.PgqlConnection;
import oracle.pgx.api.*;
import oracle.pgx.config.*;
import java.nio.file.*;

var jdbcUrl = "jdbc:oracle:thin:@//aquiles001.sii.cl:1525/grafosdb";
var user    = "beuser";
var pass    = "sii#2024";

/* ========= Conexión JDBC + PGQL (para DDL) ========= */
var conn     = DriverManager.getConnection(jdbcUrl, user, pass);
conn.setAutoCommit(false);
var pgql     = PgqlConnection.getConnection(conn);
var pgqlStmt = pgql.createStatement();

System.out.println("✅ Conectado. PGQL listo.");

/* === 1) DROP del property graph en catálogo (idempotente) ============== */
try {
  pgqlStmt.execute("DROP PROPERTY GRAPH GE_TEST_GRAPH");
  System.out.println("🗑️ GE_TEST_GRAPH eliminado del catálogo.");
} catch (Exception e) {
  System.out.println("ℹ️ GE_TEST_GRAPH no existía en catálogo (ok).");
}

/* === 2) CREATE del property graph leyendo el DDL externo =============== */
var ddlPath = Paths.get("scripts/create_ge_model.pgql");
var ddlText = Files.readString(ddlPath);   // sin ';' al final
pgql.prepareStatement(ddlText).execute();
conn.commit();            // fija el DDL para otras sesiones
pgqlStmt.close();
System.out.println("✅ GE_TEST_GRAPH creado en catálogo desde " + ddlPath);

/* Mitigar ORA-01466: breve espera */
try { Thread.sleep(800); } catch (InterruptedException ie) {}

/* === 3) Limpieza de memoria PGX local (no afecta a otras sesiones) ===== */
try {
  var gOld = session.getGraph("GE_TEST_GRAPH");
  if (gOld != null) {
    gOld.destroy();
    System.out.println("🧹 Memoria PGX local limpia.");
  } else {
    System.out.println("ℹ️ No había grafo en memoria.");
  }
} catch (Exception e) {
  System.out.println("ℹ️ Limpieza PGX ignorada: " + e.getMessage());
}

/* === 4) Carga del grafo en PGX (sin publicar) ========================== */
var b = GraphConfigBuilder.forPropertyGraphRdbms();
b.setJdbcUrl("jdbc:oracle:thin:@aquiles001.sii.cl:1525/grafosdb");
b.setUsername(user);
b.setPassword(pass);
b.setName("GE_TEST_GRAPH");
b.setLoadVertexLabels(true);
b.setLoadEdgeLabel(true);
var cfg = b.build();

/* Reintento ante ORA-01466 */
oracle.pgx.api.PgxGraph g = null;
try {
  g = session.readGraphWithProperties(cfg);
} catch (Exception e1) {
  var msg = String.valueOf(e1);
  if (msg.contains("ORA-01466")) {
    System.out.println("⚠️ ORA-01466 detectado. Reintentando tras breve espera...");
    try { Thread.sleep(1000); } catch (InterruptedException ie) {}
    g = session.readGraphWithProperties(cfg);
  } else {
    throw e1;
  }
}

System.out.println("✅ GE_TEST_GRAPH cargado en memoria (sin publicar).");
System.out.println("🌐 Session ID: " + session.getId());

/* === 5) Helper de PGQL (para que puedas probar consultas altiro) ======= */
var pgql2 = PgqlConnection.getConnection(conn);
java.util.function.Consumer<String> query = q -> {
  try (var stmt = pgql2.prepareStatement(q)) {
    stmt.execute();
    var rs = stmt.getResultSet();
    if (rs != null) rs.print();
  } catch (Exception e) {
    System.err.println("❌ PGQL: " + e.getMessage());
  }
};
System.out.println("✅ query.accept(...) listo.");


/*version final */
