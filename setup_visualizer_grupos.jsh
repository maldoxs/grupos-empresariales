/*****************************************************
 * setup_visualizer_grupos.jsh
 * Carga el grafo GRUPOS_EMPRESARIALES con todas sus propiedades
 * de vértices y aristas, y lo publica para visualización.
 *****************************************************/

import oracle.pgx.api.*;
import oracle.pgx.config.*;
import java.util.function.Supplier;

// Configuración explícita para cargar el grafo desde la base de datos
Supplier<GraphConfig> pgxConfigSupplier = () -> {
  return GraphConfigBuilder.forPropertyGraphRdbms()
      .setJdbcUrl("jdbc:oracle:thin:@aquiles001.sii.cl:1525/grafosdb")
      .setUsername("beuser")
      .setPassword("sii#2024")
      .setName("GRUPOS_EMPRESARIALES")
      // --- CARGA EXPLÍCITA DE PROPIEDADES DE LOS VÉRTICES ---
      .addVertexProperty("RUT", PropertyType.LONG)
      .addVertexProperty("RAZON_SOCIAL", PropertyType.STRING)
      .addVertexProperty("TIPO_PERSONA", PropertyType.STRING)
      .addVertexProperty("SUBTIPO", PropertyType.STRING)
      .addVertexProperty("ES_VIGENTE", PropertyType.STRING)
      .addVertexProperty("TAMANO_EMPRESA", PropertyType.STRING)
      .addVertexProperty("CLASIFICACION_RIESGO", PropertyType.STRING)
      .addVertexProperty("GRUPO_DECLARADO", PropertyType.STRING)
      // =====================================================================
      // CARGA EXPLÍCITA DE PROPIEDADES DE LAS ARISTAS (LA CORRECCIÓN CLAVE)
      // =====================================================================
      .addEdgeProperty("PORCENTAJE_PARTICIPACION", PropertyType.DOUBLE)
      .addEdgeProperty("FUENTE_INFORMACION", PropertyType.STRING)
      .addEdgeProperty("PERIODO_RELACION", PropertyType.INTEGER)
      // Aseguramos que las etiquetas de los vértices y aristas se carguen
      .setLoadVertexLabels(true)
      .setLoadEdgeLabel(true)
      .build();
};

// Forzar la recarga del grafo para asegurar que esté actualizado
// Primero, intentamos destruir cualquier versión antigua que exista en memoria.
try {
    var oldGraph = session.getGraph("GRUPOS_EMPRESARIALES");
    oldGraph.destroy();
    System.out.println("🗑️ Versión antigua del grafo en memoria eliminada.");
} catch (Exception e) {
    System.out.println("⚠️ No había una versión anterior del grafo en memoria.");
}

// Volvemos a cargar y publicar la versión más reciente desde la base de datos.
var graph = session.readGraphWithProperties(pgxConfigSupplier.get());
System.out.println("✅ Grafo GRUPOS_EMPRESARIALES cargado en memoria con todas sus propiedades.");

graph.publish(VertexProperty.ALL, EdgeProperty.ALL);
System.out.println("✅ Nueva versión del grafo publicada para visualización.");

System.out.println("🌐 Session ID (pégalo en Graph Visualization): " + session.getId());
