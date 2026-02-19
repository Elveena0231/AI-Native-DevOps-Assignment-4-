-- Minimal schema for the custom plugin; extend if you add config fields
return {
  name = "custom",
  fields = {
    { config = {
        type = "record",
        fields = {},
      }
    }
  }
}
