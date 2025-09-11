import oracle.pgx.api.*;
import oracle.pgx.config.*;
import java.util.function.Supplier;

// --- SOLUCIÓN FINAL Y COMPATIBLE ---

// PASO 1: Cargar la versión actualizada del grafo desde la base de datos.
// Usamos tu configuración original, que es la correcta y completa.
Supplier<GraphConfig> pgxConfigSupplier = () -> {
  return GraphConfigBuilder.forPropertyGraphRdbms()
      .setJdbcUrl("jdbc:oracle:thin:@aquiles001.sii.cl:1525/grafosdb")
      .setUsername("beuser")
      .setPassword("sii#2024")
      .setName("HR_BE")
      .addVertexProperty("FIRST_NAME", PropertyType.STRING)
      .addVertexProperty("LAST_NAME", PropertyType.STRING)
      .addVertexProperty("EMAIL", PropertyType.STRING)
      .addVertexProperty("PHONE_NUMBER", PropertyType.STRING)
      .addVertexProperty("SALARY", PropertyType.DOUBLE)
      .addVertexProperty("DEPARTMENT_NAME", PropertyType.STRING)
      .addVertexProperty("JOB_TITLE", PropertyType.STRING)
      .addVertexProperty("CITY", PropertyType.STRING)
      .addVertexProperty("COUNTRY_NAME", PropertyType.STRING)
      .addVertexProperty("REGION_NAME", PropertyType.STRING)
      .setLoadVertexLabels(true)
      .setLoadEdgeLabel(true)
      .build();
};

var graph = session.readGraphWithProperties(pgxConfigSupplier.get());
System.out.println("✅ Grafo recargado desde la base de datos con todas sus propiedades.");

// PASO 2: Intentar publicar, manejando el caso "already published" con try/catch.
// Esta es la única forma robusta y compatible con tu versión de la API.
try {
  graph.publish(VertexProperty.ALL, EdgeProperty.ALL);
  System.out.println("✅ Grafo publicado para visualización.");
} catch (Exception e) {
  if (e.getMessage().contains("already published")) {
    System.out.println("✅ CONFIRMADO: El grafo ya estaba publicado. Script finalizado correctamente.");
  } else {
    // Si es un error diferente, sí lo mostramos.
    System.err.println("❌ Ocurrió un error inesperado al publicar: " + e.getMessage());
  }
}

System.out.println("🌐 Session ID (pégalo en Graph Visualization): " + session.getId());
