/*****************************************************
 * setup_visualizer_ge_model_explicit.jsh
 * Igual a tu ejemplo “que funciona”, pero apuntando a GE_TEST_GRAPH.
 *****************************************************/

import oracle.pgx.api.*;
import oracle.pgx.config.*;
import java.util.function.Supplier;

// 1) limpia memoria
try {
  var old = session.getGraph("GE_TEST_GRAPH");
  if (old != null) {
    old.destroy();
    System.out.println("🗑️ Versión antigua del grafo eliminada.");
  }
} catch (Exception e) {
  System.out.println("ℹ️ No había versión anterior en memoria.");
}

// 2) Configuración EXPRESA de propiedades
Supplier<GraphConfig> pgxConfigSupplier = () -> {
  return GraphConfigBuilder.forPropertyGraphRdbms()
      .setJdbcUrl("jdbc:oracle:thin:@aquiles001.sii.cl:1525/grafosdb")
      .setUsername("beuser")
      .setPassword("sii#2024")
      .setName("GE_TEST_GRAPH")
      // Vértices (ajusta a tus labels/columnas reales en el DDL/vistas):
      .addVertexProperty("CODIGO",                 PropertyType.LONG)
      .addVertexProperty("GEMP_NOMBRE",           PropertyType.STRING)
      .addVertexProperty("GEMP_VERSION_VIGENTE",  PropertyType.INTEGER)
      .addVertexProperty("GEMP_FECHA_CREACION",   PropertyType.TIMESTAMP)
      .addVertexProperty("GEMP_FECHA_MODIFICACION", PropertyType.TIMESTAMP)
      .addVertexProperty("DISPLAY_NAME",          PropertyType.STRING)
      .addVertexProperty("GREM_ESTADO",           PropertyType.STRING)
      .addVertexProperty("GREM_VERSION",          PropertyType.DOUBLE)
      .addVertexProperty("GEMP_CODIGO",           PropertyType.LONG)
      .addVertexProperty("GREM_CODIGO",           PropertyType.LONG)
      .addVertexProperty("GPAR_RUT",              PropertyType.LONG)
      .addVertexProperty("GPAR_DV",               PropertyType.STRING)
      .addVertexProperty("GDET_TIPO_ENTIDAD",     PropertyType.STRING)
      .addVertexProperty("GLNG_CODIGO",           PropertyType.INTEGER)
      .addVertexProperty("GDET_CAPITAL_ENTERADO", PropertyType.LONG)
      .addVertexProperty("GDET_TEXTO_LIBRE",      PropertyType.STRING)
      .addVertexProperty("GDET_SOSTENIBILIDAD",   PropertyType.STRING)
      // Aristas
      .addEdgeProperty("GREM_PARTICIPACION",      PropertyType.STRING)
      .addEdgeProperty("PARTICIPACION_NUM",       PropertyType.DOUBLE)
      .addEdgeProperty("GREM_UTILIDADES",         PropertyType.STRING)
      // hace visibles los labels en memoria/visor
      .setLoadVertexLabels(true)
      .setLoadEdgeLabel(true)
      .build();
};

// 3) Cargar y publicar
var graph = session.readGraphWithProperties(pgxConfigSupplier.get());
System.out.println("✅ GE_TEST_GRAPH cargado en memoria con propiedades explícitas.");
graph.publish(VertexProperty.ALL, EdgeProperty.ALL);
System.out.println("✅ GE_TEST_GRAPH publicado para visualización.");
System.out.println("🌐 Session ID: " + session.getId());
